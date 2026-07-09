Aim: Tool to validate/suggest if your repo fulfills minimal standard requirements for a good repo (separate for matlab, python, R) that you can use as verification.

Claude Flow-chart: [https://claude.ai/design/p/55a6a247-0019-462a-a6a5-bf86af3beae5?file=Repository+Good-Practice+Check.html\&via=share](https://claude.ai/design/p/55a6a247-0019-462a-a6a5-bf86af3beae5?file=Repository+Good-Practice+Check.html&via=share)

https://selinazitrone.github.io/tools\_and\_tips/

Requirements: AI integrated IDLE (z.b: claude, github copilot) to run the agent → free version should be sufficient (to check)

Proof-of-concept: 

Resources for requirement research:

| Link | Description |
| :---- | :---- |
| https://bids-standard.github.io/bids-validator/  | Example validation for another application case (checking correctness of data format standard BIDS) |
| [https://github.com/education/students](https://github.com/education/students) | Github education for using github copilot for free |
| [Research compendia](https://research-compendium.science/)  | Research compendia  |
| [template collection](https://github.com/topics/research-compendium/) | of research compendia on Github |
| [The Turing Way](https://book.the-turing-way.org/reproducible-research/compendia/) | guide to research compendia |
|  [Nice slide show](https://mbjoseph.github.io/intro-research-compendia/) | on building research compendia step by step |
| [Good/Bad examples](https://app.notion.com/p/Good-vs-bad-repos-32168cc8955c8084ab87dbf0ad4ba3f5) | good/bad examples repo |
| [Folder Structure example](https://cookiecutter-data-science.drivendata.org/)  |  |

**Checking categories**

- **Environment/System/Installation** instructions  
  - requirements.txt / environment.yml exists (minimal)  
  - Pre-built container with all software dependencies exists (including version numbers) (advanced)  
  - Additional toolboxes needed are specified (minimal)  
  - Programming languages \+ versions specified (advanced)  
  - OS compatibility specified (minimal)  
  - Installation instructions exist in README? (minimal)  
    - Do they work? (advanced)

- **Reproducibility**  
  - Is explained how the code can be re-run? (minimal)  
  - Is the execution order clear? (minimal)  
  - Info about where (input) data can be found (minimal)  
  - If original data can not be shared, is there an explanation of how the input data have to look like (e.g., format, level of processing)? (minimal)  
  - Try a re-run (using the provided input data) → does it work? Give feedback  
    → requires IDE-integrated AI (advanced)  
- For complex projects/tools (advanced)  
  - Quick-start example exists  
  - Workflow automation available 

- **Naming and XXX:**  
  - Does the repository have a meaningful name? (minimal)  
  - Are files organized in a conventional folder structure? (minimal)  
  - Are folder- and file names meaningful? / Do they represent their content? (minimal)  
  - Is the repo as clean and easy to use as possible? (minimal)

- **README**  
  - Does a README exist? (minimal)  
  - Does the Readme contain content? (minimal)  
  - Does the README contain   
    - **Title** (minimal)  
    - **Project Description** (minimal)  
    - **Table of Contents** (advanced)  
    - **Folder/File Structure Tree** (advanced)  
      - Python ML specific: [https://cookiecutter-data-science.drivendata.org/](https://cookiecutter-data-science.drivendata.org/) (remove data folder if not publicly sharable), alternative: use repository structure from here: https://github.com/lciernik/attentive-layer-fusion  
    - **Nice to have** (advanced)  
      - Example execution command  
      - Expected outputs documented  
      - Citation information  
      - Versioned releases

- **Professionality**  
  - No tipos (minimal)  
  - Use of Markdown (for fonts, …) (advanced)  
  - Visualizations (advanced)

- **Code Quality** (advanced)  
  - meaningful variable names   
  - comments explaining methodology   
  - clear separation between (processing) stages 

- **Licence** (minimum)  
  - Licence guide: \[insert link\]  
      
- **Example Data**   
  - Simulated or synthetic

1. Requirements (Deadline: 26.06)  
2. Korrekte Integration in .skill prompt  
3. Report shiny  
4. Portable options with instruction (claude, copilot)  
5. README repo-validation-tool  
   1. Add a concise visualization of what the tool is doing at the top (e.g. a brief horizontal flowchart)  
   2. Add a citation of the tool as ‘Research Software’ (cite it if you used it to check your repository before publication)

Meine Kollegin hatte letztens bei einer submission diese Code+Software Submission Check-Liste von Nature zugesendet bekommen. Wir decken das alles ab, könnten überlegen, ob wir das zitieren oder erwähnen im README, dass wir diese Checklist (neben anderen Punkten) vollständig abdecken.  
![][image1]

1\. [https://github.com/neurodata-papers/MGC](https://github.com/neurodata-papers/MGC)

2\. [https://github.com/neurodata-papers/LOL](https://github.com/neurodata-papers/LOL)

3\. [https://www.nature.com/nbt/journal/v34/n6/abs/nbt.3569.html\#supplementary-information](https://www.nature.com/nbt/journal/v34/n6/abs/nbt.3569.html#supplementary-information)

4\. [https://www.nature.com/nature/journal/v548/n7669/full/nature23463.html\#extended-data](https://www.nature.com/nature/journal/v548/n7669/full/nature23463.html#extended-data)  
[https://github.com/yasharhezaveh/Ensai](https://github.com/yasharhezaveh/Ensai)

5\. [https://www.nature.com/nbt/journal/v34/n11/full/nbt.3685.html\#supplementary-information](https://www.nature.com/nbt/journal/v34/n11/full/nbt.3685.html#supplementary-information)  
[https://github.com/IFIproteomics/LFQbench](https://github.com/IFIproteomics/LFQbench)  
