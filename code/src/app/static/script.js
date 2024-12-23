let selectedTool = 'elements'; // Set default tool to 'elements'
let currentDocuments = {}; // Store documents globally
let activeSection = null; // Track the currently active section

// Fetch documents from the server and populate tabs
fetch('/api/documents')
    .then(response => response.json())
    .then(documents => {
        currentDocuments = documents; // Save the documents for future reference
        const tabList = document.getElementById('tab-list');
        tabList.innerHTML = '';

        // Filter only section documents for the tabs
        const sections = Object.values(documents).filter(doc => doc.type === 'section');
        sections.forEach((section, index) => {
            const listItem = document.createElement('li');
            const link = document.createElement('a');
            link.href = "#";
            link.textContent = section.id;
            link.className = index === 0 ? 'active' : ''; // Set the first tab active by default
            link.addEventListener('click', (e) => {
                e.preventDefault();
                setActiveTab(link);
                activeSection = section; // Track the active section
                loadSection(section);
            });
            listItem.appendChild(link);
            tabList.appendChild(listItem);

            // Automatically load the first section with default tool selected
            if (index === 0) {
                activeSection = section; // Set the first section as active
                loadSection(section);
            }
        });

        // Select the default tool "Elements extraction and classification"
        selectTool('elements');
    })
    .catch(error => {
        console.error("Error loading documents:", error);
    });

// Set the clicked tab as active
function setActiveTab(activeLink) {
    const links = document.querySelectorAll('.tabs ul li a');
    links.forEach(link => link.classList.remove('active'));
    activeLink.classList.add('active');
}

// Load a section content
function loadSection(section) {
    console.log("Loading section:", section); // Debug checkpoint
    const sectionContainer = document.getElementById('section-content');
    sectionContainer.innerHTML = ''; // Clear previous content

    // Add the section content
    const sectionParagraph = document.createElement('p');
    sectionParagraph.textContent = section.content;
    sectionContainer.appendChild(sectionParagraph);

    // Display the section content container
    sectionContainer.style.display = 'block';

    // Load additional content based on the selected tool
    loadToolContent();
}

// Load tool content into its dedicated area
function loadToolContent() {
    const toolContentContainer = document.getElementById('tool-content');
    const toolHeader = document.getElementById('tool-header');
    const toolBody = document.getElementById('tool-body');
    
    toolBody.innerHTML = ''; // Clear previous tool content

    if (selectedTool === 'elements' && activeSection) {
        console.log("Tool 'Elements extraction and classification' selected, rendering tool content."); // Debug checkpoint

        // Update and show the tool header
        toolHeader.textContent = "Elements extraction and classification";
        toolHeader.style.display = 'flex';

        // Check for related llm_response content
        const relatedResponses = Object.values(currentDocuments).filter(
            doc => doc.type === 'llm_response' && doc.content.section === activeSection.id
        );

        // Render llm_response highlights if found
        relatedResponses.forEach(response => {
            renderLlmResponse(response.content, toolBody);
        });

        // Display the tool content container
        toolContentContainer.style.display = 'block';
    } else {
        console.log("No relevant tool selected, hiding tool content."); // Debug checkpoint
        toolContentContainer.style.display = 'none';
        toolHeader.style.display = 'none'; // Hide the header when no tool is active
    }
}

// Render llm_response highlights
function renderLlmResponse(content, container) {
    // Add the summary with "Summary:" at the beginning
    const summaryParagraph = document.createElement('p');
    summaryParagraph.style.fontWeight = 'bold';
    summaryParagraph.textContent = "Summary: " + content.summary;
    container.appendChild(summaryParagraph);

    // Render each element
    content.elements.forEach(element => {
        const statementParagraph = document.createElement('p');
        statementParagraph.style.backgroundColor = 'lightyellow';
        statementParagraph.style.padding = '10px';
        statementParagraph.style.margin = '10px 0';
        statementParagraph.innerHTML = highlightStatement(element);
        container.appendChild(statementParagraph);
    });
}

// Highlight and format statement
function highlightStatement(element) {
    let statement = element.statement;

    // Highlight terms
    element.terms.forEach(term => {
        if (term.classification === 'Common Noun') {
            const regex = new RegExp(`\\b${term.term}\\b`, 'g');
            statement = statement.replace(
                regex,
                `<span style="text-decoration: underline; text-decoration-color: green;">${term.term}</span>`
            );
        } else if (term.classification === 'Proper Noun') {
            const regex = new RegExp(`\\b${term.term}\\b`, 'g');
            statement = statement.replace(
                regex,
                `<span style="text-decoration: underline double; text-decoration-color: green;">${term.term}</span>`
            );
        }
    });

    // Highlight verb symbols
    element.verb_symbols.forEach(verb => {
        const regex = new RegExp(`\\b${verb}\\b`, 'g');
        statement = statement.replace(
            regex,
            `<span style="font-style: italic; color: blue;">${verb}</span>`
        );
    });

    // Add source at the beginning of the statement
    const sourceText = `<strong>[${element.sources}]</strong> `;
    statement = sourceText + statement;

    // Add superscript classification
    const superscript = `<sup style="cursor: help;" title="${element.classification === 'Fact Type' ? 'FT: Fact Type' : 'OP: Operative Rule'}">${element.classification === 'Fact Type' ? 'FT' : 'OP'}</sup>`;
    statement += superscript;

    return statement;
}

// Tool selection function
function selectTool(tool) {
    // Update the selected tool to the new one
    selectedTool = tool;

    // Update UI to reflect tool selection
    const tools = document.querySelectorAll('.sidebar ul li a');
    tools.forEach(link => link.classList.remove('active-tool'));
    const selectedLink = document.getElementById(`tool-${tool}`);
    if (selectedLink) {
        selectedLink.classList.add('active-tool');
    }

    // Reload the tool content in the dedicated area
    loadToolContent();
}
