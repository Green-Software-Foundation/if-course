# Impact Framework Fundamentals
## Comprehensive Course Outline

### Target Audience
- **Software Engineers** and **DevOps Professionals** seeking to measure and reduce the environmental impact of their applications
- **Sustainability Officers** and **Green IT Specialists** looking for practical tools to calculate software carbon emissions
- **Technical Managers** wanting to implement environmental impact tracking in their development practices
- **Prerequisites**: Basic understanding of YAML, command-line tools, and software architecture. Node.js experience helpful but not required.

### Course Description

Impact Framework Fundamentals is a hands-on course that teaches you how to measure, calculate, and report the environmental impacts of software applications using the Impact Framework (IF) — an open-source tool developed by the Green Software Foundation.

Through practical exercises and a comprehensive walkthrough, you'll learn to create Impact Manifest Protocol (IMP) files that transform observational data into carbon emissions measurements. The course covers direct and proxy measurements, the Software Carbon Intensity (SCI) specification, and advanced topics like time-series data handling and multi-component aggregation. By the end, you'll be able to conduct full environmental impact investigations for real-world applications.

### Duration
- **Total Time**: 12-15 hours of content
- **Recommended Schedule**: 3-4 weeks (3-4 hours per week)
- **Self-paced**: Complete at your own speed with hands-on exercises

---

## Module Breakdown

### **Module 1: Quickstart**
*Duration: 45-60 minutes*

#### Learning Objectives:
- Install and configure Impact Framework on your local machine
- Execute your first Impact Manifest Protocol (IMP) file
- Understand the relationship between manifest files and their outputs
- Visualize impact calculations using the IF Visualizer
- Modify assumptions and observe how they affect results

#### Key Topics:
- Installing IF via npm
- Understanding IMP file structure (context vs. tree)
- Running `if-run` command and interpreting output
- Using the IF Visualizer to explore results
- The concept of executable and auditable manifest files
- Modifying grid carbon intensity assumptions

#### Practical Assignment:
Run the provided quickstart manifest for the GSF website, modify the `grid/carbon-intensity` value to represent your local region, and observe how the carbon emissions change. Document your findings in a short report comparing the baseline (global average 494 gCO2e/kWh) to your regional value.

---

### **Module 2: Essential Concepts**
*Duration: 30-45 minutes*

#### Learning Objectives:
- Understand the core design philosophy of Impact Framework
- Distinguish between observations, impacts, plugins, models, and pipelines
- Learn how components and groupings structure your system
- Understand the role of IMP files in transparent impact calculation
- Define what an "investigation" means in the IF context

#### Key Topics:
- Design principles: Transparency, Verifiability, Flexibility, Modularity, Neutrality
- Observations vs. Impacts
- Plugins, Models, and Pipelines
- Components and Grouping hierarchies
- IMP file structure (context and tree sections)
- The IDOMI investigation process

#### Quiz:
1. What is the difference between an observation and an impact?
2. How does a plugin differ from a model in Impact Framework?
3. Name three design principles of Impact Framework and explain one.
4. What are the two main sections of an IMP file?
5. Why is the pipeline concept important for transparency?

---

### **Module 3: Direct Measurement (One-Step Pipeline)**
*Duration: 90-120 minutes*

#### Learning Objectives:
- Apply the IDOMI process (Impacts, Dependencies, Observations, Methodology, Implementation)
- Create a complete IMP file from scratch
- Configure and use the `Multiply` builtin plugin
- Build impact dependency trees to plan calculations
- Execute manifest files and interpret outputs

#### Key Topics:
- IDOMI process introduction
- Building impact dependency trees
- Creating boilerplate IMP files
- Configuring plugins in the `initialize` section
- Adding observations to component inputs
- Creating compute pipelines
- Understanding execution and output sections
- Direct energy measurement to carbon calculation

#### Practical Assignment:
Create your own manifest file for a hypothetical server where you have direct energy measurements (0.08 kWh) and local carbon intensity data. Calculate the carbon emissions for a 2-hour observation period. Bonus: Try using the `Coefficient` plugin instead of `Multiply` to achieve the same result.

---

### **Module 4: Proxy Measurements**
*Duration: 90-120 minutes*

#### Learning Objectives:
- Convert indirect metrics (like memory utilization) into energy estimates
- Chain multiple plugins together in a pipeline
- Use the `Coefficient` and `Sum` builtin plugins
- Understand proxy measurement methodologies
- Build multi-step pipelines for complex calculations

#### Key Topics:
- What are proxy measurements and when to use them
- Memory utilization to energy conversion (CCF coefficient method)
- Chaining plugins: plugin order matters
- Combining multiple energy sources (CPU + memory)
- Using the `Sum` plugin for aggregation
- Reading and citing methodology sources

#### Quiz:
Multiple choice questions covering:
- Definition of proxy measurements
- Application of memory utilization coefficients
- Plugin chaining and the `Sum` plugin
- Calculating combined energy values
- Importance of transparent methodology documentation

---

### **Module 5: Understanding Software Carbon Intensity (SCI)**
*Duration: 60-90 minutes*

#### Learning Objectives:
- Understand the SCI formula: `SCI = (E * I + M) per R`
- Learn the components: operational energy (E), carbon intensity (I), embodied carbon (M), and functional unit (R)
- Understand the SCI specification and its ISO standard status
- Use the `Sci` and `SciEmbodied` builtin plugins
- Define appropriate software boundaries and functional units

#### Key Topics:
- SCI formula breakdown and component definitions
- Why offsets are excluded from SCI
- The SCI specification (ISO/IEC 21031:2024)
- SCI for X: domain-specific implementations
- SCI Guidance project resources
- Defining software boundaries in IMP files
- Embodied carbon and the CCF model
- Selecting functional units (per user, per request, per visit, etc.)
- The `Sci` and `SciEmbodied` plugins

#### Practical Assignment:
Complete the provided partial IMP file by adding the `sci` plugin configuration to calculate carbon per request. The manifest should compute energy from CPU utilization, then carbon from energy, and finally SCI per request.

---

### **Module 6: SCI Walkthrough - Planning (IDO)**
*Duration: 60-75 minutes*

#### Learning Objectives:
- Plan a complete SCI calculation for a realistic server scenario
- Build comprehensive impact dependency trees
- Identify all required observations for an SCI calculation
- Map cloud infrastructure observations to impacts
- Create the foundational structure for a full SCI manifest

#### Key Topics:
- Applying IDOMI to SCI calculations
- Building complete dependency trees for SCI
- Identifying operational and embodied carbon dependencies
- Planning functional unit observations
- Sourcing cloud provider metadata (instance type, region, etc.)
- Using `defaults` for static configuration
- Complete observation inventory for SCI

#### Practical Assignment:
Create an impact dependency tree for your own application or a hypothetical e-commerce API server. Identify: (1) available observations, (2) required dependencies, (3) missing data that would need estimation, and (4) an appropriate functional unit.

---

### **Module 7: SCI Walkthrough - Operational Energy**
*Duration: 90-120 minutes*

#### Learning Objectives:
- Convert CPU utilization into energy using TDP and power curves
- Use the `Interpolation` plugin for power curve calculations
- Query external datasets with the `CSVLookup` plugin
- Understand the Teads power curve methodology
- Combine CPU and memory energy into total operational energy
- Convert power (Watts) to energy (kWh)

#### Key Topics:
- Memory utilization to energy conversion (coefficient method)
- CPU utilization to energy (power curve method)
- Thermal Design Power (TDP) and TDP multipliers
- The Teads generalized power curve
- Using `CSVLookup` to query cloud instance metadata
- The `Interpolation` plugin for power curves
- Power vs. Energy: Understanding the distinction
- Unit conversions (W to Wh to kWh)
- Summing energy components

#### Practical Assignment:
Modify the provided manifest to use a different Azure instance type (e.g., Standard_D4s_v3). Research the TDP of its processor and update the cloud metadata CSV lookup. Compare the operational energy results between instance types at the same CPU utilization.

---

### **Module 8: SCI Walkthrough - Operational Carbon**
*Duration: 45-60 minutes*

#### Learning Objectives:
- Convert operational energy into operational carbon using carbon intensity
- Query the Real Time Cloud (RTC) dataset for carbon intensity values
- Use CSV column renaming with tuple syntax in `CSVLookup`
- Multiply energy by carbon intensity to calculate operational carbon
- Understand regional and temporal carbon intensity variations

#### Key Topics:
- Carbon intensity data sources (WattTime, Electricity Maps, RTC)
- The GSF Real Time Cloud dataset
- CSV tuple syntax for column renaming: `['original-name', 'output-name']`
- Querying by multiple fields (cloud-provider AND cloud-region)
- Annual average vs. real-time carbon intensity
- Operational carbon calculation: `operational-energy * carbon-intensity`

#### Practical Assignment:
Add a second server component to your manifest in a different Azure region (e.g., `eastus` instead of `westeurope`). Compare the operational carbon between regions at identical CPU utilization levels. Research and explain why the carbon intensity differs.

---

### **Module 9: SCI Walkthrough - Embodied Carbon**
*Duration: 60-75 minutes*

#### Learning Objectives:
- Understand embodied carbon and why it's difficult to measure
- Apply the Cloud Carbon Footprint (CCF) embodied carbon model
- Use the `SciEmbodied` builtin plugin
- Research and specify hardware configurations (vCPUs, memory, SSD, HDD, GPU)
- Extend CSV lookups to retrieve multiple columns with renaming

#### Key Topics:
- Embodied carbon definition and lifecycle assessment (LCA)
- The CCF baseline server model
- Component-specific carbon additions (CPU, memory, storage, GPU)
- The `SciEmbodied` plugin configuration
- Required parameters: vCPUs, memory, ssd, hdd, gpu, duration
- Multi-column CSV output with tuple syntax
- Researching cloud instance specifications
- When to seek vendor-specific embodied carbon data

#### Practical Assignment:
Research the hardware specifications for a different cloud instance (AWS EC2 or Google Cloud). Create a manifest calculating its embodied carbon using `SciEmbodied`. Compare the embodied carbon per hour between your instance and the Azure Standard_A2m_v2 used in the walkthrough.

---

### **Module 10: SCI Walkthrough - Completing the SCI Score**
*Duration: 45-60 minutes*

#### Learning Objectives:
- Combine operational and embodied carbon into total carbon
- Apply the `Sci` plugin to calculate the final SCI score
- Understand the complete SCI pipeline from observations to score
- Interpret SCI results in context (gCO2e per functional unit)
- Validate a complete end-to-end SCI calculation

#### Key Topics:
- Summing operational and embodied carbon
- The `Sci` plugin configuration with functional units
- Why `carbon` must be the parameter name for the Sci plugin
- Complete manifest walkthrough (all 11 plugins)
- Interpreting SCI output: what does "0.41 gCO2e per visit" mean?
- The full IDOMI implementation review

#### Practical Assignment:
Take the complete SCI manifest from this module and modify it to calculate SCI per different functional units:
1. SCI per request (assuming 50 requests per visit)
2. SCI per hour (time-based SCI)
Compare and explain the differences in the resulting SCI scores.

---

### **Module 11: Working with Time Series Data**
*Duration: 45-60 minutes*

#### Learning Objectives:
- Add multiple observations to the `inputs` array
- Understand how IF processes time-series data independently
- Interpret varying SCI scores across time periods
- Recognize patterns in operational vs. embodied carbon over time
- Handle multi-day or multi-week observations

#### Key Topics:
- Multiple entries in the `inputs` array
- Independent pipeline execution per observation
- Timestamp and duration specifications
- Varying observations: CPU utilization, memory, functional unit counts
- Why embodied carbon remains constant across observations
- Interpreting time-series SCI results
- When high carbon doesn't mean bad efficiency

#### Practical Assignment:
Extend your SCI manifest to cover one week (7 days) of observations. Use realistic varying CPU utilization (e.g., weekday peaks, weekend lows). Create a table showing: date, CPU%, site visits, operational carbon, embodied carbon, and SCI. Write a brief analysis identifying the most and least carbon-efficient days.

---

### **Module 12: Synchronizing Time Series with Time-Sync**
*Duration: 60-75 minutes*

#### Learning Objectives:
- Understand the problem of misaligned time series across components
- Configure the `TimeSync` builtin plugin
- Align multiple components to a common time window
- Understand padding behavior for missing timesteps
- Prepare time-synchronized data for aggregation

#### Key Topics:
- The time-alignment problem with multiple components
- `TimeSync` plugin configuration: start-time, end-time, interval, allow-padding
- Adding `time-sync` to pipelines (must be first!)
- How padding works: copying nearest observation
- Global time windows vs. component-specific observations
- When to use TimeSync: multi-component scenarios

#### Practical Assignment:
Create a manifest with three server components, each with different observation periods:
- Server A: 00:00-02:00 (2 hours)
- Server B: 01:00-03:00 (2 hours)
- Server C: 02:00-04:00 (2 hours)

Use TimeSync to align them to a global window of 00:00-04:00. Verify that all three servers have four output observations. Identify which observations were padded and explain the values used.

---

### **Module 13: Aggregation**
*Duration: 45-60 minutes*

#### Learning Objectives:
- Understand time-series (horizontal) aggregation
- Understand tree (vertical) aggregation
- Configure aggregation in IMP files
- Interpret aggregated results at component and root levels
- Calculate total carbon and average SCI across time periods and components

#### Key Topics:
- Types of aggregation: `time`, `component`, and `both`
- The `aggregation` section configuration
- Specifying metrics to aggregate (carbon, sci, energy, etc.)
- Component-level `aggregated` fields
- Root-level `outputs` and `aggregated` sections
- Summing carbon vs. averaging SCI
- Multi-component fleet-wide totals

#### Practical Assignment:
Take your multi-server manifest from Module 12 and add aggregation configuration for carbon and SCI. Run the manifest and answer:
1. What is the total carbon across all servers and all timesteps?
2. What is the average SCI score for the fleet?
3. Which server had the highest total carbon? The best SCI?
Write a one-page summary report with these findings.

---

### **Module 14: Planning an Investigation**
*Duration: 90-120 minutes*

#### Learning Objectives:
- Define application boundaries for complex systems
- Design component hierarchies and grouping strategies
- Apply IDOMI to multiple diverse components
- Plan observation strategies for different component types
- Scale from single-component to multi-component investigations
- Create investigation scopes for real applications

#### Key Topics:
- Three phases of investigation: Scoping, IDOMI per component, Execution
- Application boundary definition (what's in scope?)
- Components and grouping design for actionable insights
- Functional unit selection and availability
- Observation types: direct, indirect, heuristic
- Per-component IDOMI application
- Example: GSF website investigation
- Different methodologies for different components (server, network, devices)
- When to use coefficients vs. complex models

#### Practical Assignment:
**Capstone Project Setup**: Choose a real or realistic application to investigate:
- E-commerce website
- Mobile app with API backend
- Data processing pipeline
- ML training workflow

Create a comprehensive investigation plan including:
1. Application boundary definition (list all components)
2. Component hierarchy/grouping structure
3. Chosen functional unit with justification
4. Per-component observation audit (what data is available?)
5. High-level methodology notes for each component

Submit this as a 2-3 page planning document.

---

### **Module 15: Wrap Up & Next Steps**
*Duration: 45-60 minutes*

#### Learning Objectives:
- Review the complete IDOMI workflow from modules 1-14
- Learn to use `if-check` for verification
- Explore the IF Visualizer in depth
- Understand paths for continued learning
- Learn about the SCI Certificate of Disclosure program
- Discover community resources and contribution opportunities

#### Key Topics:
- Course recap: From single plugin to complete investigations
- The IF Visualizer deep dive
- Using `if-check` for manifest verification
- The executable audit concept
- Contributing to IF-DB repository
- Peer review of community investigations
- SCI Certificate of Disclosure program
- Plugin Explorer and community plugins
- SCI Guidance resources
- Green Software Foundation community

#### Final Project:
Complete your capstone investigation from Module 14:
1. Implement your investigation plan as IMP file(s)
2. Execute and generate output manifests
3. Visualize results using the IF Visualizer
4. Write a 3-5 page report including:
   - Executive summary of findings
   - Methodology explanation
   - Results with visualizations
   - Recommendations for carbon reduction
5. Submit your manifest files and report

**Bonus**: Share your investigation with the IF-DB repository following the contribution guidelines.

---

## Additional Course Features

### Prerequisites Checklist
- [ ] Node.js v16 or higher installed
- [ ] Basic command-line proficiency
- [ ] Text editor or IDE installed
- [ ] Understanding of YAML syntax
- [ ] Familiarity with software architecture concepts

### Recommended Tools
- **Code Editor**: VS Code with YAML extensions
- **Terminal**: Any bash-compatible terminal
- **Browser**: Modern browser for visualizer access
- **Optional**: Git for cloning example repositories

### Support Resources
- Official IF Documentation: https://if.greensoftware.foundation/
- Plugin Explorer: https://explorer.if.greensoftware.foundation/
- SCI Guidance: https://sci-guide.greensoftware.foundation/
- IF-DB Examples: https://github.com/Green-Software-Foundation/if-db
- Course Repository: Includes all source manifests and datasets

### Certification Path
Upon completion, learners will be prepared to:
- Conduct professional software carbon audits
- Contribute to open-source environmental impact tooling
- Pursue SCI Certificate of Disclosure for their organizations
- Mentor others in green software practices

---

**Course Version**: Based on Impact Framework v1.1.0+
**Last Updated**: February 2026
**Maintained by**: Green Software Foundation
