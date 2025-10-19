# **[Cableteque Bicycle Configurator](https://cabletequebicycle.streamlit.app/)**

A small toolkit + Streamlit (https://cabletequebicycle.streamlit.app/) app that reads a compact Excel specification of bicycle modifications (an `ID` sheet plus `GENERAL` and designator sheets), generates every possible bicycle permutation, and exports the result as JSON (and CSV). This repository contains:

* `BicycleConfigurator.py` - core Python module (function `generate_bicycles_from_sheets(xlsx_path) -> str`). Streamlit app for uploading .xlsx, previewing, filtering and downloading results.
* `requirements.txt` - environment d ependencies.
* Example Excel template: `Bicycle_example.xlsx` (downloadable from the app sidebar).
## A brief video tutorial showcasing the application's features and usage is available here: **[Watch the Tutorial](https://drive.google.com/file/d/1_Z6KOhkGKJjfnBUtLVUcGi14ZWTx_ep3/view?usp=sharing)**

## Key features

* Reads an Excel workbook with a multi-sheet structure:
  
  * `ID` sheet - each column is a *designator*; rows are possible values. All combinations are created by taking one value from each column.
  * `GENERAL` sheet - common fields applied to every bike.
  * Component Sheets: All other sheets map a specific designator value (first column) to its detailed attributes (subsequent columns).
* Generates the Cartesian product of all designator values and merges component-specific fields into each final bicycle object.
* Produces clean, ready-to-use data exports, including a well-structured JSON string (list of objects) and a universally compatible CSV file.
* Interactive Streamlit UI:

  * Upload your .xlsx file and generate thousands of permutations directly in the browser.
  * Set a custom ID separator (e.g., -, _, or blank) to format the output IDs.
  * Choose a conflict resolution strategy to manage how data from different sheets is prioritized.
  * Filter and explore the generated data with dynamic, searchable dropdowns for any attribute.
  * Inspect the complete data for any single bicycle by selecting its ID.

---

## Business Value & Use Cases

* `For Product & Inventory Teams`: Drastically reduce manual data entry by defining thousands of product variations in a single, intuitive Excel file, instantly generating a complete and error-free digital catalog.
* `For Development & Engineering`: Utilize the clean JSON or CSV output as a single source of truth to power front-end product pages, populate search databases, or integrate directly with backend ERP and inventory systems.
* `For Business Stakeholders`: Empower non-technical users to self-serve. The interactive Streamlit application allows anyone to upload a file and generate the data they need without writing a single line of code.

---

## Quickstart - run locally

1. Create and activate a virtual environment (optional, recommended):

   ```bash
   python -m venv venv
   # Unix / macOS
   source venv/bin/activate
   # Windows (PowerShell)
   .\\venv\\Scripts\\Activate.ps1
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:

   ```bash
   streamlit run BicycleConfigurator.py
   ```

   Visit `http://localhost:8501` in your browser.

4. Upload your Excel file (structure explained above) and use the UI to preview and download `bicycles.json` or `bicycles.csv`.

---

## Command-line usage

If you only want the core generator (no UI), use `bicycle_generator.py` functions from your own script or run the included self-test by executing:

```bash
python BicycleConfigurator.py
```

Or call the core function from another Python program:

```python
from bicycle_generator import generate_bicycles_from_excel
json_str = generate_bicycles_from_excel("/absolute/path/to/Bicycle.xlsx")
print(json_str)
```

---
## Acknowledgements

I would like to extend my heartfelt gratitude to the entire team at Cableteque for this wonderful opportunity.

Your trust and encouragement have been truly motivating and working on this project has been both an inspiring and enriching experience.

This project allowed me to sharpen my technical expertise while also reflecting on how I can personally grow in alignment with your values of innovation, collaboration and positive impact.

I am eager to work with Cableteque, learn from the team’s wealth of experience, and contribute meaningfully towards your mission of building a more sustainable and innovative future.
## Design & implementation notes

* The generator builds the Cartesian product using `itertools.product`.
* General fields are applied first, and then per-designator sheets are applied in a deterministic order. The Streamlit UI lets you choose which precedence strategy to use.
* The Streamlit app includes accessibility checks (contrast ratio) and a set of curated theme presets to avoid poor color combinations.
* If the number of permutations grows very large, the app will still work but may become slow or heavy on memory, consider reducing the number of values per designator or adding serverside limits for deployment.

---

## How I align with Cableteque's mission, values & vision

Cableteque champions deep domain knowledge, practical innovation, and building tools that genuinely help engineers and manufacturing teams work better. I strongly identify with these priorities, and my personal values and working style map closely to Cableteque’s PIA framework and broader mission:

* **Pioneering (P)** - I embrace innovation and forward-thinking approaches. I enjoy exploring new ideas, automating repetitive tasks, and pushing boundaries to make workflows simpler and more powerful.

* **Insightful (I)** - I am committed to continuous learning. I actively seek new perspectives, study domain-specific practices (such as product configuration and inventory workflows), and apply lessons learned to improve both technical solutions and user experiences.

* **Agile (A)** - I work iteratively and adapt to change. I favor practical, incremental improvements, rapid prototyping, and close feedback loops so that solutions remain simple, useful, and easy to adopt.

Beyond the PIA framework, I also align with Cableteque’s broader cultural values:

* **Inclusivity & collaboration:** I enjoy working with diverse teams, listening to domain experts, and incorporating their feedback into the product. I believe great solutions come from shared expertise.

* **Sustainability & positive impact:** I aim to build tools that reduce wasteful manual work and enable teams to focus on higher-value tasks.

* **Trust & shared success:** I prioritize clear communication, reliable tooling, and thoughtful design so teams can depend on the software and succeed together.

My mindset is centered on practical innovation, continuous learning, and collaborative delivery—fits naturally with Cableteque’s mission and values. I’m excited by opportunities to contribute in environments that prize domain expertise, user-first tools, and iterative improvement.

---

## Credits

* Developed by: **Gourang Agarwal** (project author)


---

## Contact

* LinkedIn: **[Gourang Agarwal](https://www.linkedin.com/in/gourang4/)**
