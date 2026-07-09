# The repo-reviewer tool

Summary of architecture and choices so far \+ open questions to discuss

## Overview and requirements

**What it does:** Review scientific data-analysis repository before publication and write one [REVIEW.md](http://REVIEW.md). The review doc is a prioritised checklist of what to improve. The tool is language agnostic and works for R, Python, or other repos. Focus is on data-analysis repos but in theory can also be run on other software repos. Later there can also be a website that explains the review criteria/checklist in more details and list some good external resources

**What it does not do:**

- Run the code: checks reviewability and completeness but not reproducibility  
- Does not give scores/badges: checks are not 100% objective and reproducible. Some are AI judgements. At maximum we could give something like 7/9 criteria met.  
- Modify the repo: Does not help users fix the problems in the repo. Only writes [REVIEW.md](http://REVIEW.md)

**Selling point:** Yes this is AI, but the backbone are our researched and categorized checklist items. The AI will only rely on those items and will be kept on a short leash. This means that the tool will be somewhat transparent and reliable although it’s AI.

**Requirements to run the tool:** AI-integrated IDE (for now Claude Code, but also Github Copilot works) \+ the repo to review

## The criteria for review

The criteria are the checklist items that the repo-reviewer checks against. They should be **categorized** and **ranked** in a systematic way. If the criteria are clearly described and systematically written down, the AI has less room for speculation and the tool will be more precise and trustworthy.

The idea for now (details below):

- Criteria are divided into groups by topic  
- Criteria are categorized by severity  
- Criteria have different modes: deterministic/ai/none  
- One markdown file per criteria structured clearly with YAML header for the AI and prose text for the website later

###  Topic groups

See also: criteria/\_groups.md

- Orientation: README, purpose, repo structure and file names, contact, …  
- Licensing and citation: LICENCE, data licence, CITATION.cff  
- Data: availability statement, sensitive data flag, separation of raw/derived data, …  
- Code and analysis: structure, naming, absolute paths, seeds, comments, run order, …  
- Environment: dependencies and versions, container, language version, …  
- Repository hygiene: any junk files/dead files, any secrets (e.g. API keys, etc.), …  
- Archive and release: Zenodo/DOI,...

### Severity scale

Criteria are marked by severity:

- must-fix: without it, a stranger cannot reuse the repo  
- Should-fix: reuse is possible but harder than necessary  
- Polish: everything else

### Criteria modes

- Deterministic: Criteria can be checked without AI (e.g. README/LICENCE present yes/no)  
- AI: Criteria is evaluated with AI judgement (e.g. is the README clear, are the file names good, …)  
- None: Criteria that cannot be checked by AI (e.g. is it on Zenodo and has a DOI)

### How to document the criteria

We have a standardised way to document criteria in a markdown file with YAML header.

- YAML header: Will be compiled into the criterion catalogue used by AI  
- Prose text: Can be used for the website

See also:

- \_schema.md for an overview how the schema looks like right now  
- criteria/ for some worked examples of criteria

## The AI skill

- As deterministic/reproducible as possible:   
  - File & pattern checks run deterministically from a small script (e.g. to check if README exists) \-\> This avoids AI hallucinations  
- Avoid hallucinations: AI skill should just audit the repo based on our criteria. It should only raise a point if that point is part of our defined check list, every finding must cite concrete file-path evidence. If there is no evidence, there is no finding.  
- Uncertainty should be visible: If a check cannot be decided, it should be marked

### The workflow

![][image2]

- Skill is compiled from a **skill template** and the **criteria files** \-\> Different skill templates depending on the goal (Claude Skill, GH Copilot prompt, Copyable prompt  
- If skill is run in local environment: Use a simple check script for deterministic checks (e.g. README present/not present) \-\> This produces a temporary JSON that the AI Skill uses to judge deterministic criteria  
  - Cannot be used if the checker is a copyable prompt e.g. for Chat GPT, then the fallback should be AI checks rather than deterministic checks

## The report template

- See example in the repo REVIEW-scales\_3d.md

For now it’s just a md file

Basic idea:

- Intro section  
  - Top: Info to delete file before publishing  
  - Context info: What is checked, which model was used  
  - Summary of the repo: The model writes what it understands from the repo  
- “Do this first” section  
  - All must-fix actions with info on how to fix  
- “Checklist”  
  - All checklist items sorted by category  
  - Marked: ✅ pass · ❌ needs fixing · ⚠️ couldn't verify · ➖ not applicable  
- “Before you publish”  
  - All items that cannot be checked e.g. Zenodo/DOI, …  
- Outro section  
  - Maybe a X/X criteria passing  
  - Used model, date, criteria version

## Open questions

- Website (Quarto?): Can be part of the same repo and contain:  
  - Installation/Usage guides for different versions of the skill  
  - The criteria but written with more prose for people to read details (can be compiled from the criteria markdown files \- not the YAML part but the body)  
  - Links to additional resources and other tools  
- Validation and testing  
  - Use the good/bad repos listed above \-\> Many of them are not data-analysis but software/packages  
  - Can we get a good list of repositories from different fields, languages and quality? They could also be used to tell AI to further refine the criteria or adjust the report where needed  
  - How to validate?  
    - Run on same repo multiple times and check if the report is consistent?  
    - Compare hand-made report with AI-report? \-\> Hand made report should be done before AI report

## Next steps

### First

- Decide on the architecture  
- Tightly define criteria using a structured schema  
- Validate and test thoroughly

### Next

- Adjust to other AI providers  
- Website guides  
- Report format \-\> Keep md? Some people might not like the way it looks and are not able to render it nicely. But giving the report as a pdf or html takes more effort from the AI, more tokens, more tools (e.g. Quarto to render md to pdf/html)
