let firstDocData = {};   // The doc data from the first selected file
let otherDocsData = {};  // The doc data from all selected files, used for comparison
let activeSection = null;
let selectedTool = 'elements';

function loadFirstDocument(filename, restoreSectionId = null) {
  fetch(`/api/single_document?filename=${encodeURIComponent(filename)}`)
    .then(res => res.json())
    .then(data => {
      firstDocData = data;
      buildTabs(restoreSectionId); // Pass restoreSectionId to maintain the active tab
    })
    .catch(err => console.error("Error loading first doc:", err));
}

function buildTabs(restoreSectionId = null) {
  const tabList = document.getElementById('tab-list');
  tabList.innerHTML = '';

  const sections = Object.values(firstDocData).filter(doc => doc.type === 'section');
  let foundActive = false;

  sections.forEach((sec, idx) => {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = "#";
    a.textContent = sec.id;

    if (restoreSectionId && sec.id === restoreSectionId) {
      a.className = 'active';
      activeSection = sec;
      foundActive = true;
    } else if (!restoreSectionId && idx === 0) {
      a.className = 'active';
      activeSection = sec;
    }

    a.addEventListener('click', e => {
      e.preventDefault();
      setActiveTab(a);
      activeSection = sec;
      loadSectionContent(sec);
    });
    li.appendChild(a);
    tabList.appendChild(li);
  });

  if (restoreSectionId && !foundActive && sections.length > 0) {
    const firstLink = tabList.querySelector('li:first-child a');
    if (firstLink) {
      firstLink.classList.add('active');
      activeSection = sections[0];
    }
  }

  if (activeSection) loadSectionContent(activeSection);
}

function setActiveTab(link) {
  const allLinks = document.querySelectorAll('#tab-list li a');
  allLinks.forEach(l => l.classList.remove('active'));
  link.classList.add('active');
}

// Show the text of the chosen section
function loadSectionContent(section) {
  const sectionContainer = document.getElementById('section-content');
  sectionContainer.innerHTML = `<p>${section.content}</p>`;
  loadToolContent();
}

// Re-render the tool area (elements, etc.) for the current section
function loadToolContent() {
  const toolContent = document.getElementById('tool-content');
  const toolHeader = document.getElementById('tool-header');
  const toolBody = document.getElementById('tool-body');
  toolBody.innerHTML = '';

  if (selectedTool === 'elements' && activeSection) {
    toolHeader.textContent = "Elements extraction and classification";
    toolHeader.style.display = 'flex';
    toolContent.style.display = 'block';

    const responses = Object.values(firstDocData).filter(
      doc => doc.type === 'llm_response' && doc.content.section === activeSection.id
    );

    responses.forEach(resp => {
      renderLlmResponse(resp.content, toolBody);
    });
  } else {
    toolContent.style.display = 'none';
    toolHeader.style.display = 'none';
  }
}

// Renders a single llm_response from the first doc + side-by-side from other docs
function renderLlmResponse(responseContent, parent) {
  parent.innerHTML = '';

  const multipleFilesSelected = Object.keys(otherDocsData).length > 0;

  if (!multipleFilesSelected) {
    // Single file selected: Render only the primary document
    responseContent.elements.forEach(elem => {
      const elemDiv = document.createElement('div');
      elemDiv.innerHTML = `<p>${highlightStatement(elem)}</p>`;
      parent.appendChild(elemDiv);
    });
  } else {
    // Multiple files selected: Align elements side by side
    responseContent.elements.forEach(elem => {
      const block = document.createElement('div');
      block.className = 'comparison-block';

      // The column for the primary document (first file)
      const primaryDocCol = document.createElement('div');
      primaryDocCol.innerHTML = `
        <div class="title">Primary Document</div>
        <div>${highlightStatement(elem)}</div>
      `;
      block.appendChild(primaryDocCol);

      // Columns for other selected documents
      Object.entries(otherDocsData).forEach(([filename, docData]) => {
        const sameSectionResp = Object.values(docData).find(
          d => d.type === 'llm_response' && d.content.section === activeSection.id
        );

        let statementHTML = `No matching section in ${filename}`;
        if (sameSectionResp) {
          const foundEl = sameSectionResp.content.elements.find(e => e.id === elem.id);
          if (foundEl) {
            statementHTML = highlightStatement(foundEl);
          } else {
            statementHTML = `No matching element for ID ${elem.id}`;
          }
        }

        const col = document.createElement('div');
        col.innerHTML = `
          <div class="title">${filename}</div>
          <div>${statementHTML}</div>
        `;
        block.appendChild(col);
      });

      parent.appendChild(block);
    });
  }
}

// Basic function to highlight each statement
function highlightStatement(element) {
  let text = element.statement;

  // Underline terms
  element.terms.forEach(term => {
    const regex = new RegExp(`\\b${term.term}\\b`, 'g');
    if (term.classification === 'Common Noun') {
      text = text.replace(
        regex,
        `<span style="text-decoration: underline; text-decoration-color: green;">${term.term}</span>`
      );
    } else if (term.classification === 'Proper Noun') {
      text = text.replace(
        regex,
        `<span style="text-decoration: underline double; text-decoration-color: green;">${term.term}</span>`
      );
    }
  });

  // Italicize verb symbols
  element.verb_symbols.forEach(verb => {
    const regex = new RegExp(`\\b${verb}\\b`, 'g');
    text = text.replace(
      regex,
      `<span style="font-style: italic; color: blue;">${verb}</span>`
    );
  });

  // Put ID at the front
  text = `${element.id} ${text}`;

  // Classification
  const sup = `<sup style="cursor:help" title="${
    element.classification === 'Fact Type' ? 'FT: Fact Type' : 'OP: Operative Rule'
  }">${element.classification === 'Fact Type' ? 'FT' : 'OP'}</sup>`;
  text += sup;

  // Remove brackets from sources
  if (typeof element.sources === 'string') {
    const clean = element.sources.replace(/^\[|\]$/g, '');
    text += ` <strong>${clean}</strong>`;
  }
  return text;
}

// Switch the tool
function selectTool(tool) {
  selectedTool = tool;
  const allToolLinks = document.querySelectorAll('.sidebar ul li a');
  allToolLinks.forEach(l => l.classList.remove('active-tool'));
  const chosenLink = document.getElementById(`tool-${tool}`);
  if (chosenLink) chosenLink.classList.add('active-tool');

  if (activeSection) {
    loadToolContent();
  }
}

// On page load, populate the multi-select
window.addEventListener('DOMContentLoaded', () => {
  const fileSelector = document.getElementById('file-selector');

  fetch('/api/list_files')
    .then(res => res.json())
    .then(files => {
      fileSelector.innerHTML = '';
      files.forEach(f => {
        const opt = document.createElement('option');
        opt.value = f;
        opt.text = f;
        fileSelector.appendChild(opt);
      });

      if (files.length > 0) {
        fileSelector.value = files[0];
        Array.from(fileSelector.options).forEach(o => {
          o.selected = o.value === files[0];
        });
        loadFirstDocument(files[0]);
        fetch('/api/multiple_documents', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ files: [files[0]] })
        })
          .then(res => res.json())
          .then(data => {
            otherDocsData = data;
          });
      }
    })
    .catch(err => console.error("Error listing files:", err));

  fileSelector.addEventListener('change', () => {
    const selected = Array.from(fileSelector.selectedOptions).map(o => o.value);

    if (selected.length === 0) {
      firstDocData = {};
      otherDocsData = {};
      activeSection = null;
      document.getElementById('tab-list').innerHTML = '';
      document.getElementById('section-content').innerHTML = '';
      document.getElementById('tool-body').innerHTML = '';
      return;
    }

    const currentSectionId = activeSection ? activeSection.id : null;
    const mainFile = selected[0];
    loadFirstDocument(mainFile, currentSectionId);

    fetch('/api/multiple_documents', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ files: selected })
    })
      .then(res => res.json())
      .then(data => {
        otherDocsData = data;
        loadToolContent();
      })
      .catch(err => console.error("Error fetching multiple docs:", err));
  });
});
