# Definition
## 9.2 Definitional rules
Definitional rules constrains how we define a construct created or used by the organization or the industry within which it operates. Definitional rules can in turn be categorized as:
### 9.2.1 Formal term definitions:
A formal term definition defines a particular business term in a formal manner. They are categorized as:
#### 9.2.1.1 Formal intensional definitions
A formal intensional definition defines the subject business term using an intensional definition: one that cites both a hypernym (a term that refers to a superset of the set referred to by the original term) and the characteristics that distinguish members of the set referred to by the original term.
T7.
```template
{A|An} <term 1>
	{of {a|an} <term 2>| }
is by definition
{a|an|the} <term 3>
	<qualifying clause>.
```
#### 9.2.1.2 Formal extensional definitions
Formal extensional definition defines the subject business term by using an extensional definition: one that lists a complete set of hyponyms (terms that refer to subsets of the set referred to by the original term).
T8.
```template
{A|An} <term 1>
	{of {a|an} <term 2>| }
is by definition
[<article> <term 3>, or]
	{of that <term 2>| }.
```
#### 9.2.1.3 Symbolic literal definitions
A symbolic literal definition defines the subject business term using one or more literals.
T9.
```template
{<literal 1>|{A|An} <term 1>
	{of {a|an} <term 2>| }}
is by definition
{<literal 2>|
[<literal 3>, or] from a <literal 4> to the following <literal 5>}.
```
### 9.2.2 Categorization scheme enumerations
A categorization scheme enumeration defines the members of a categorization scheme that is both mutually exclusive and jointly exhaustive.
T10.
```template
{{A|An} <category attribute term>|
The <category attribute term>
	of {a |an} <entity class term>}
is by definition
{either <literal 1> or <literal 2>|
one of the following: [<literal 3>, or]}.
```
### 9.2.3 Category transition constraints
A category transition constraint specifies allowed or disallowed transitions between categories or statuses.
T11.
```template
A transition
	of the <category attribute term> of {a|an} <entity class term>
	from {<literal 1>| [<literal 2>, or]}
	to {<literal 3>| [<literal 4>, or]}
is by definition
impossible.
```
### 9.2.4 Complex concept structure rules
A complex concept structure rule defines a particular constraint on one or more components of a complex concept. They are categorized as:
#### 9.2.4.1 Complex concept cardinality rules
A complex concept cardinality rule defines the number of (or minimum and/or maximum number of) components of a particular type within a particular concept.
T12.
```template
{A|An} <term 1>
<verb phrase> by definition
{<cardinality>|at most <positive integer>} <term 2>
	{{for |in} {each|the} <term 3>| }.
```
#### 9.2.4.2 Complex concept equivalence rules
A complex concept equivalence rule defines a pair of components within a particular concept that are of necessity the same.
T13.
```template
The <term 1>
	<qualifying clause 1>
is by definition
the same as the <term 2>
	<qualifying clause 2>.
```
#### 9.2.4.3 Complex concept set constraints
A complex concept set constraint defines two sets of components within a particular concept that must be identical.
T14.
```template
The set of <term 1>
	<qualifying clause 1>
is by definition
the same as the set of <term 1>
	<qualifying clause 2>.
```
### 9.2.5 Valid value definitions
A valid value definition defines the valid values of a particular measure as a range or (occasionally) as a list of discrete values.
T15.
```template
{The| } <attribute term>
	{of {a|an} <entity class term>| }
is by definition
{<inequality operator> <literal 1>
	{and <inequality operator> <literal 2>| } |
	[<literal 3>, or]}.
```
### 9.2.6 Data calculation rules
A data calculation rule defines the algorithm or formula for a particular quantity or a conversion factor between two units. They are categorized as:
#### 9.2.6.1 Data calculation algorithms
A data calculation algorithm defines how a particular quantity or amount (whether for operational purposes, such as a fee, or for business intelligence purposes, such as a performance measure) is calculated.
T16.
```template
{The| } <attribute term>
	{of | for} {a|an} <entity class term>
	{<qualifying clause>| }
is by definition calculated as
<expression>.
```
#### 9.2.6.2 Conversion factor definitions
A conversion factor definition defines a conversion factor between two units of measurement.
T17.
```template
<literal 1>
is by definition {approximately | } equal to
<literal 2>.
```
### 9.2.7 Standard format definitions
A standard format definition defines the standard format for data items of a particular type in terms of individual characters and/or component data items.
T18.
```template
A valid <term>
is by definition composed of
<format definition>.
```
## 9.3 Data rules
Data rules (all of which are operative rules) constrains the data included in a transaction (a form or message) or a persistent dataset (e.g., a database record). Data rules can in turn be categorized as:
### 9.3.1 Data cardinality rules
A data cardinality rule requires the presence or absence of a data item and/or places a restriction on the maximum or minimum number of occurrences of a data item
#### 9.3.1.1 Mandatory data rules
A mandatory data rule mandates the presence of data:
##### 9.3.1.1.1 Mandatory data item rules
A mandatory data item rule requires that a particular data item be present.
T19.
```template
Each <transaction signifier>
must {specify|contain} <cardinality> <data item term>
	{{in| for} {each|the} <subform term> {(if any)| }
	{<qualifying clause>| } | }
{{if |unless} <conditional clause>| }.
```
##### 9.3.1.1.2 Mandatory option selection rules
A mandatory option selection rule requires that one of a set of pre-defined options be specified.
with two or more options:
T20.
```template
Each <transaction signifier>
must
{({if |unless} <conditional clause>) | }
specify whether {it |{the |each} <term>
	{<qualifying clause>| }}
<verb phrase> [<object>, or].
```
with a single option:
T21.
```template
Each <transaction signifier>
must
{({if |unless} <conditional clause>) | }
specify whether {or not| } {it |{the |each} <term>
	{<qualifying clause>| }}
<verb phrase> {<object>| }.
```
##### 9.3.1.1.3 Mandatory group rules: 
A mandatory group rule requires that at least one of a group of data items be present.
two data items in the group:
T22.
```template
Each <transaction signifier>
must {specify|contain}
	{{in| for} {each|the} <subform term> {(if any)| }
	{<qualifying clause>| } | }
	{a|an} <data item term 1>, {a|an} <data item term 2>
	{, or|but not} both
{{if |unless} <conditional clause>| }.
```
more than two data items in the group:
T23.
```template
Each <transaction signifier>
must
{({if |unless} <conditional clause>) | }
{specify |contain}
	{{in| for} {each|the} <subform term> {(if any)| }
	{<qualifying clause>| } | }
	<cardinality> of the following:
	[<data item term>, or].
```
#### 9.3.1.2 Prohibited data rules
A prohibited data rule mandates the absence of some data item in a particular situation.
T24.
```template
{A|An} <transaction signifier>
must not {specify |contain} a <data item term>
	{{in | for} {any|the} <subform term> {(if any)| }
	{<qualifying clause>| } | }
{{if |unless} <conditional clause>| }.
```
#### 9.3.1.3 Maximum cardinality rules
A maximum cardinality rule places an upper limit (usually but not necessarily one) on how many instances of a particular data item there may be.
T25.
```template
{A|An} <transaction signifier>
must not {specify |contain} more than <positive integer>
	<data item term>
	{{in | for} {any one|the} <subform term> {(if any)| }
	{<qualifying clause>| } | }
{{if |unless} <conditional clause>| }.
```
#### 9.3.1.4 Multiple data rules
A multiple data rule mandates the presence of two or more instances of a particular data item in a particular situation.
T19.
```template
Each <transaction signifier>
	must {specify|contain} <cardinality> <data item term>
	{{in| for} {each|the} <subform term> {(if any)| }
	{<qualifying clause>| } | }
{{if |unless} <conditional clause>| }.
```

these rule statements `<cardinality>` may only take one of the following forms:
1. exactly `<positive integer>`, where `<positive integer>` is at least two;
2. at least `<positive integer>`, where `<positive integer>` is at least two;
3. at least `<positive integer 1>` and at most `<positive integer 2>`, where `<positive integer 1>` is at least two.
#### 9.3.1.5 Dependent cardinality rules
A dependent cardinality rule mandates how many of a particular data item must be present based on the value of another data item.
T26.
```template
The number of <data item term 1>
	{specified|contained}
	{{in| for} {the|each} <subform term> {(if any) | } | }
	in each <transaction signifier>
must be {{no|} {more|less} than|equal to} the <data item term 2>
	{<qualifying clause>| }
{{if |unless} <conditional clause>| }.
```
### 9.3.2 Data content rules
A data content rule places a restriction on the values contained in a data item or set of data items (rather than whether they must be present and how many there may or must be).
#### 9.3.2.1 Value set rules
A value set rule requires either: that the content of a data item be (or not be) one of a particular set of values (either a fixed set, or a set that may change over time), or; that the content of a combination of data items match or not match a corresponding combination in a set of records;
##### 9.3.2.1.1 Value set rules constraining single data items
T27.
```template
{The|Each} <data item term> {(if any)| }
	specified {{in| for} {the|each} <subform term> {(if any)| } | }
	in each <transaction signifier>
must be
	{{other than| } one of the <term> <qualifying clause>| [<literal>, or]}
{{if |unless} <conditional clause>| }.
```
##### 9.3.2.1.2 Value set rules constraining combinations of data items
T28.
```template
{The|Each} combination of [<data item term 1>, and] {(if any)| }
	specified {{in| for} {the|each} <subform term> {(if any)| } | }
	in each <transaction signifier>
must be one of the combinations of [<data item term 2>, and]
	{<qualifying clause>| }
{{if |unless} <conditional clause>| }.
```
#### 9.3.2.2. Range rules
A range rule requires that the content of a data item be a value within a particular inclusive or exclusive single-bounded or double-bounded range.
T29.
```template
{The|Each} <data item term> {(if any)| }
	specified {{in| for} {the|each} <subform term> {(if any)| } | }
	in each <transaction signifier>
must be <inequality operator> <object> {and <inequality operator> <object>| }
{{if |unless} <conditional clause>| }.
```
#### 9.3.2.3 Equality rules
An equality rule requires that the content of a data item be the same as or not the same as that of some other data item.
T30.
```template
{The|Each} <data item term> {(if any)| }
	specified {{in| for} {the|each} <subform term> {(if any)| } | }
	in each <transaction signifier>
must be <equality operator> <object>
{{if |unless} <conditional clause>| }.
```
#### 9.3.2.4 Uniqueness constraints
A uniqueness constraint requires that the content of a data item (or combination or set of data items) be different from that of the corresponding data item(s) in the same or other records or transactions;
##### 9.3.2.4.1 Uniqueness constraints constraining single data items.
T31.
```template
{The|Each} <data item term 1> {(if any)| }
	<verb part> {the <subform term 1> {(if any)| }
	in|} each <transaction signifier 1>
	{<qualifying clause 1>| }
must be different from the <data item term 1>
	<verb part> {{the |any other} <subform term 1> {(if any)| }
	in| } {that |any other} <transaction signifier 1>
	{<qualifying clause 2>| }
{{if |unless} <conditional clause>| }.
```
##### 9.3.2.4.2 Uniqueness constraints constraining combinations of data items
T32.
```template
{The|Each} combination of [<data item term 1>, and] {(if any)| }
	<verb part> {the <subform term 1> {(if any)| }
	in| } each <transaction signifier 1>
	{<qualifying clause 1>| }
must be different from the combination of [<data item term 1>, and]
	<verb part> {{the|any other} <subform term 1> {(if any) | }
	in| } {that |any other} <transaction signifier 1>
	{<qualifying clause 2>| }
{{if |unless} <conditional clause>| }.
```
##### 9.3.2.4.3 Uniqueness constraints constraining sets of data items
T33.
```template
{The|Each} set of <data item term 1> {(if any)| }
	<verb part> {the <subform term 1> {(if any)| }
	in|} each <transaction signifier 1>
	{<qualifying clause 1>| }
must be different from the set of <data item term 1>
	<verb part> {{the |any other} <subform term 1> {(if any)| }
	in| } {that |any other} <transaction signifier 1>
	{<qualifying clause 2>| }
{{if |unless} <conditional clause>| }.
```
#### 9.3.2.5 Data consistency rules
A data consistency rule requires the content of multiple data items to be consistent with each other, other than as provided for by a value set rule, range rule, or equality rule;
##### 9.3.2.5.1 Data consistency rules constraining a combination of data items
T34.
```template
{The|Each} combination of [<data item term>, and] {(if any)| }
	specified {{in| for} {the|each} <subform term> {(if any)| } | }
	in each <transaction signifier>
	{<qualifying clause>| }
must be such that <conditional clause 1>
{{if |unless} <conditional clause 2>| }.
```
##### 9.3.2.5.2 Data consistency rules constraining a set function
T35.
```template
The <set function> of {the| } <data item term> {(if any)| }
	specified {{in| for} {the|each} <subform term> {(if any)| } | }
	in each <transaction signifier>
	{<qualifying clause>| }
must be {<inequality operator>|<equality operator>} <object>
{{if |unless} <conditional clause>| }.
```
##### 9.3.2.5.3 Data consistency rules constraining a set
T36.
```template
{The|Each} set of <data item term> {(if any)| }
	specified {{in| for} {the|each} <subform term> {(if any)| } | }
	in each <transaction signifier>
	{<qualifying clause 1>| }
must {be {the same as| different from} |include} the set of <term>
	{<qualifying clause 2>| }
{{if |unless} <conditional clause>| }.
```
#### 9.3.2.6 Temporal data constraints
A temporal data constraint constrains one or more temporal data items (data items that represent time points or time periods). There are various subcategories of temporal constraint:
##### 9.3.2.6.1 Simple temporal data constraints
A simple temporal data constraint requires that a particular date or time fall within a certain temporal range.
T29.
```template
{The|Each} <data item term> {(if any)| }
	specified {{in| for} {the|each} <subform term> {(if any)| } | }
	in each <transaction signifier>
must be <temporal inequality operator> <object> {and <temporal inequality operator> <object>| }
{{if |unless} <conditional clause>| }.
```
R373.
```example
The departure time of the outgoing flight
	specified in each flight booking confirmation
	that is made online
must be no earlier than 3 h
	after the booking confirmation time
	of that flight booking confirmation.
```
##### 9.3.2.6.2 Temporal data non-overlap constraints
Temporal data non-overlap constraint requires that the time periods specified in a set of records do not overlap each other.
T37.
```template
{The|Each} <time period term 1> {(if any)| }
	specified {{in| for} {the|each} <subform term 1> {(if any)| } | }
	in each <transaction signifier 1>
	{<qualifying clause 1>| }
must not overlap the <time period term 1>
	specified {{in| for} {the|each} <subform term 1> {(if any)| } | }
	in any other <transaction signifier 1>
	{<qualifying clause 2>| }
{{if |unless} <conditional clause>| }.
```
##### 9.3.2.6.3 Temporal data completeness constraints
A temporal data completeness constraint requires that the time periods specified in a set of records be contiguous and between them completely span some other time period.
T38.
```template
Each <time period term 1>
	within the <time period term 2> {(if any)| }
	specified {{in| for} {the|each} <subform term 1> {(if any)| } | }
	in each <transaction signifier 1>
	{<qualifying clause 1>| }
must be within the <time period term 3>
	specified {{in| for} {the|each} <subform term 2> {(if any)| } | }
	in <cardinality> <transaction signifier 2>
	{<qualifying clause 2>| }
{{if |unless} <conditional clause>| }.
```
##### 9.3.2.6.4 Temporal data inclusion constraints
A temporal data inclusion constraint requires that the time periods specified in a set of records do not fall outside some other time period.
T38.
```template
Each <time period term 1>
	within the <time period term 2> {(if any)| }
	specified {{in| for} {the|each} <subform term 1> {(if any)| } | }
	in each <transaction signifier 1>
	{<qualifying clause 1>| }
must be within the <time period term 3>
	specified {{in| for} {the|each} <subform term 2> {(if any)| } | }
	in <cardinality> <transaction signifier 2>
	{<qualifying clause 2>| }
{{if |unless} <conditional clause>| }.
```
##### 9.3.2.6.5 Temporal single record constraints
A temporal single record constraint requires that a temporal state of affairs be recorded using a single record rather than multiple records.
single data item is involved:
T39.
```template
{The|Each} <data item term 1> {(if any)| }
	specified {{in| for} {the|each} <subform term 1> {(if any)| } | }
	in each <transaction signifier 1>
must be different from the <data item term 1>
	specified {{in| for} {the|each} <subform term 1> {(if any)| } | }
	in the latest of the earlier <transaction signifier 1>
{{if |unless} <conditional clause>| }.
```
combination of data items is involved:
T40.
```template
{The|Each} combination of [<data item term 1>, and] {(if any)| }
	specified {{in| for} {the|each} <subform term 1> {(if any)| } | }
	in each <transaction signifier 1>
must be different from the combination of [<data item term 1>, and]
	specified {{in| for} {the|each} <subform term 1> {(if any)| } | }
	in the latest of the earlier <transaction signifier 1>
{{if |unless} <conditional clause>| }.
```
##### 9.3.2.6.6 Day type constraints
A day type constraint restricts a date to one or more days of the week or a particular type of day such as a working day (typically but not necessarily any day other than a Saturday, Sunday, or public holiday).
T41.
```template
{The|Each} <data item term> {(if any)| }
	specified {{in| for} {the|each} <subform term> {(if any)| } | }
	in each <transaction signifier>
must be a {<term>|<literal 1>| [<literal 2>, or]}
{{if |unless} <conditional clause>| }.
```
#### 9.3.2.7 Spatial data constraints
A spatial data constraint prescribes or prohibits relationships between data items representing spatial properties (points, line segments or polygons).
T41.
```template
{The|Each|A|An} <spatial term 1> {(if any)| }
	<qualifying clause 1>
must {not| } <spatial operator> the <spatial term 2>
	<qualifying clause 2>
{{if |unless} <conditional clause>| }.
```
#### 9.3.2.8 Data item format rules
A data item format rule specifies the required format of a data item.
T43.
```template
The <data item term> {(if any)| }
	specified {{in| for} {the|each} <subform term> {(if any)| } | }
	in each <transaction signifier>
must be {represented using| } a valid <term>
{{if |unless} <conditional clause>| }.
```
### 9.3.3 Data update rules
A data update rule either prohibits update of a data item or places restrictions on the new value of a data item in terms of its existing value. There are three subcategories of data update rule:
#### 9.3.3.1 Data update prohibition rules
A data update prohibition rule prohibits update of a particular data item or set of data items.
non-transferable relationships:
T44.
```template
{A|An} <transaction signifier 1>
must not be transferred
	from one <transaction signifier 2> to another <transaction signifier 2>
{{if |unless} <conditional clause>| }.
```
other data update:
T45:
```template
{The|A|An} <data item term> {(if any)| }
	{{in |for} {any|the} <subform term> {(if any)| } | }
	{in|of} a <transaction signifier>
must not be updated
{{if |unless} <conditional clause>| }.
```
#### 9.3.3.2 State transition constraints
A state transition constraint limits the changes in a data item to a set of valid transitions.
T46.
```template
The <data item term> {(if any)| }
	{{in |for} {any|the} <subform term> {(if any)| } | }
	{in|of} a <transaction signifier>
may be updated to {<literal 1>| [<literal 2>, or]}
only if <conditional clause>.
```
#### 9.3.3.3 Monotonic transition constraints
A monotonic transition constraint requires that a numeric value either only increase or only decrease.
T47.
```template
The <data item term> {(if any)| }
	{{in| for} {any|the} <subform term> {(if any)| } | }
	{in |of} a <transaction signifier>
must not be {increased|decreased}
{{if |unless} <conditional clause>| }.
```
## 9.4 Activity rules
Activity rules (all of which are operative rules) constrains the operation of one or more business processes or other activities. Activity rules can in turn be categorized as:
### 9.4.1 Activity restriction rules
An activity restriction rule restricts a business process or other activity in some way. There are various subcategories of activity restriction rules:
#### 9.4.1.1 Rules restricting when an activity can occur
Many activity restriction rules place time restrictions on activities.
##### 9.4.1.1.1 Activity time limit rules
An activity time limit rule restricts a business process or other activity to within a particular time period.
T48.
```template
{The| } <process term> {of | for} {a|an} <object term>
	{<qualifying clause>| }
{must {not| } occur|may occur only}
<time restriction 1> {{and| or} <time restriction 2>| }
{{if |unless} <conditional clause>| }.
```
##### 9.4.1.1.2 Activity exclusion period rules
An activity exclusion period rule prohibits a business process or other activity during a particular time period.
T49.
```template
{Each|A|An} <term>
	{<qualifying clause 1>| }
{must {not| } <verb phrase 1> {<object 1>| }
	{<qualifying clause 2>| } |
may <verb phrase 2> {<object 2>| }
	{<qualifying clause 3>| } only}
<time restriction 1> {{and| or} <time restriction 2>| }
{{if |unless} <conditional clause>| }.
```
##### 9.4.1.1.3 Activity obligation rule
An activity obligation rule requires a business process or other activity to occur either within a maximum time after a particular event (such as the completion of some other process) or as soon as practical after a particular event.
T49.
```template
{Each|A|An} <term>
	{<qualifying clause 1>| }
{must {not| } <verb phrase 1> {<object 1>| }
	{<qualifying clause 2>| } |
may <verb phrase 2> {<object 2>| }
	{<qualifying clause 3>| } only}
<time restriction 1> {{and| or} <time restriction 2>| }
{{if |unless} <conditional clause>| }.
```
#### 9.4.1.2 Activity pre-condition rules
An activity pre-condition rule prohibits a business process or other activity unless some other activity or event has previously occurred or some prerequisite condition exists.
T50.
```template
{A|An} <subject term>
	{<qualifying clause>| }
may <verb phrase> {<object>| }
only {<time restriction>| if <conditional clause>}.
```
#### 9.4.1.3 Activity prohibition rules
An activity prohibition rule prohibits a business process or other activity if some event or other process has previously occurred or some dangerous or illegal condition exists.
T51.
```template
{A|An} <subject term>
	{<qualifying clause>| }
must not <verb phrase> {<object>| }
if <conditional clause>.
```
#### 9.4.1.4 Information retention rules
An information retention rule defines the minimum period for which a particular type of information is retained.
T49.
```template
{Each|A|An} <term>
	{<qualifying clause 1>| }
{must {not| } <verb phrase 1> {<object 1>| }
	{<qualifying clause 2>| } |
may <verb phrase 2> {<object 2>| }
	{<qualifying clause 3>| } only}
<time restriction 1> {{and| or} <time restriction 2>| }
{{if |unless} <conditional clause>| }.
```
#### 9.4.1.5 Activity conflict rules
An activity conflict rule restricts the simultaneous occurrence of multiple processes or other activities.
```
R136.
```example
A folder
must not be renamed
while any file within that folder is open for editing.
```
### 9.4.2 Process decision rules
A process decision rule determines what action a business process or device is to take in specific situations;
T52.
```template
Each <actor term>
must <verb phrase> {<object>| }
	{<qualifying clause>| }
{{if |unless} <conditional clause>| }.
```
### 9.4.3 Activity obligation rules
An activity obligation rule requires a business process or other activity to occur either within a maximum time after a particular event (such as the completion of some other process) or when particular conditions apply.
R138. 
```example
Each electronic device that is being used on an aircraft
must be switched off
no later than 1 min after the start of the descent of that aircraft.
```
## 9.5 Party rules
Party rules (all of which are operative rules) restricts the parties who can perform a process or activity or play a role. Party rules can in turn be categorized as
### 9.5.1 Party restriction rules
A party restriction rule places restrictions on who can perform some processes or activities or play some roles, based on age, some other physical characteristic or capability, or training, testing, and certification in the appropriate skills.
T53.
```template
A <party signifier 1>
	{<qualifying clause>| }
may <predicate 1>
only if {the <attribute signifier> of| } that <party signifier 1>
	<predicate 2>.
```
### 9.5.2 Role separation and binding rules
A role separation rule prohibits the same party from performing two activities.
T54.
```template
The <party signifier 1>
	<qualifying clause 1>
must {not| } be {the same|one of the} <party signifier 1>
	<qualifying clause 2>
{{if |unless} <conditional clause>| }.
```
### 9.5.3 Information access rules
An information access rule defines who can view, create, or update particular information.
T55.
```template
{The|A|An} <information signifier>
	<qualifying clause>
may be <information access process> by
only {<object 1>| [<object 2>, or]}
{{if |unless} <conditional clause>| }.
```
### 9.5.4 Responsibility rules
A responsibility rule defines who is responsible for performing a particular process or liable for a particular fee, duty, or tax.
T56.
```template
{The|A|An| } <responsibility signifier>
	{<qualifying clause 1>| }
must <verb phrase> {the |a|an} <party signifier>
	{<qualifying clause 2>| }
{{if |unless} <conditional clause>| }.
```
