"""
src/scraper.py
Job scraping functionality with test data for SHPE companies
"""

# Test data for all SHPE sponsor companies
SHPE_COMPANY_JOBS = [
    # Accenture
    {
        'company': 'Accenture',
        'title': 'Software Engineer - Cloud Solutions',
        'description': 'Design, build, test, and configure applications using business requirements. Work with AWS, Azure, and Google Cloud platforms. Strong proficiency in Java, Python, or C++. Experience with Agile methodologies, CI/CD pipelines, and SQL. Collaborate with cross-functional teams and provide technical solutions.'
    },
    {
        'company': 'Accenture',
        'title': 'Data Engineer',
        'description': 'Build and maintain data pipelines and ETL processes. Strong skills in Python, SQL, and big data technologies like Spark and Hadoop. Experience with cloud platforms (AWS, Azure), data warehousing, and data visualization tools like Tableau or Power BI. Knowledge of machine learning is a plus.'
    },
    
    # Edwards
    {
        'company': 'Edwards',
        'title': 'Mechanical Engineer - Medical Devices',
        'description': 'Design and develop medical device components using SolidWorks and CAD software. Conduct finite element analysis (FEA) and testing. Knowledge of GD&T, manufacturing processes, and medical device regulations (FDA, ISO 13485). Strong problem-solving and project management skills required.'
    },
    {
        'company': 'Edwards',
        'title': 'Quality Engineer',
        'description': 'Ensure product quality through statistical analysis and process improvement. Six Sigma certification preferred. Experience with quality management systems, CAPA, validation protocols, and regulatory compliance. Strong analytical skills and proficiency in Minitab or JMP.'
    },
    
    # ExxonMobil
    {
        'company': 'ExxonMobil',
        'title': 'Chemical Engineer',
        'description': 'Optimize refinery operations and process design. Strong knowledge of thermodynamics, fluid mechanics, and chemical process simulation software like Aspen Plus or HYSYS. Experience with process safety management, lean manufacturing, and data analysis using Python or MATLAB.'
    },
    {
        'company': 'ExxonMobil',
        'title': 'Petroleum Engineer',
        'description': 'Develop drilling and production strategies for oil and gas reservoirs. Knowledge of reservoir simulation software, well testing, and production optimization. Strong skills in data analysis, project management, and technical writing. Experience with Python, SQL, and visualization tools.'
    },
    
    # Bank of America
    {
        'company': 'Bank of America',
        'title': 'Software Developer - Full Stack',
        'description': 'Develop web applications using React, Angular, Node.js, and Java. Strong knowledge of RESTful APIs, microservices architecture, and SQL databases. Experience with DevOps tools like Jenkins, Docker, and Kubernetes. Agile development experience required.'
    },
    {
        'company': 'Bank of America',
        'title': 'Data Analyst',
        'description': 'Analyze financial data and create dashboards using SQL, Python, and Tableau. Strong statistical analysis skills and experience with data mining. Knowledge of machine learning, Excel advanced functions, and business intelligence tools. Excellent communication and presentation skills.'
    },
    
    # Bloomberg
    {
        'company': 'Bloomberg',
        'title': 'Software Engineer - Financial Systems',
        'description': 'Build high-performance financial applications using C++, Python, and JavaScript. Experience with real-time data processing, distributed systems, and low-latency programming. Knowledge of financial markets, algorithms, and data structures. Strong problem-solving abilities required.'
    },
    {
        'company': 'Bloomberg',
        'title': 'Data Engineer - Analytics',
        'description': 'Design scalable data infrastructure using Python, SQL, and distributed computing frameworks. Experience with data modeling, ETL pipelines, and cloud technologies (AWS, GCP). Knowledge of financial data, APIs, and real-time streaming technologies like Kafka.'
    },
    
    # CDM Smith
    {
        'company': 'CDM Smith',
        'title': 'Civil Engineer - Water Resources',
        'description': 'Design water distribution and wastewater systems using AutoCAD Civil 3D and HEC-RAS. Knowledge of hydraulic modeling, stormwater management, and environmental regulations. Strong technical writing and project management skills. PE license preferred or ability to obtain.'
    },
    {
        'company': 'CDM Smith',
        'title': 'Environmental Engineer',
        'description': 'Conduct site assessments and remediation design. Experience with environmental modeling software, NEPA compliance, and sustainability practices. Strong skills in data analysis, GIS, and technical report writing. Knowledge of water treatment and air quality regulations.'
    },
    
    # Capital One
    {
        'company': 'Capital One',
        'title': 'Machine Learning Engineer',
        'description': 'Develop ML models for fraud detection and risk assessment using Python, TensorFlow, and PyTorch. Strong knowledge of statistics, deep learning, and feature engineering. Experience with AWS, Spark, and MLOps. Familiarity with SQL and data visualization tools.'
    },
    {
        'company': 'Capital One',
        'title': 'Cloud Engineer - DevOps',
        'description': 'Build and maintain cloud infrastructure on AWS. Experience with Terraform, Docker, Kubernetes, and CI/CD pipelines. Strong scripting skills in Python or Bash. Knowledge of security best practices, monitoring tools, and agile methodologies.'
    },
    
    # GE Vernova
    {
        'company': 'GE Vernova',
        'title': 'Electrical Engineer - Power Systems',
        'description': 'Design electrical systems for power generation and distribution. Strong knowledge of power electronics, control systems, and MATLAB/Simulink. Experience with grid integration, renewable energy, and electrical simulation software. Project management and technical writing skills required.'
    },
    {
        'company': 'GE Vernova',
        'title': 'Controls Engineer',
        'description': 'Develop control algorithms for industrial systems. Experience with PLC programming (Allen-Bradley, Siemens), SCADA systems, and HMI development. Strong knowledge of automation, instrumentation, and process control. Proficiency in Python and C++ is a plus.'
    },
    
    # General Mills
    {
        'company': 'General Mills',
        'title': 'Food Process Engineer',
        'description': 'Optimize manufacturing processes for food production. Knowledge of food safety regulations (HACCP, GMP), process improvement methodologies (Lean, Six Sigma), and equipment design. Strong analytical skills and experience with AutoCAD and process simulation software.'
    },
    {
        'company': 'General Mills',
        'title': 'Supply Chain Analyst',
        'description': 'Analyze supply chain data to improve efficiency and reduce costs. Strong skills in Excel, SQL, and data visualization tools like Tableau. Experience with ERP systems (SAP), forecasting, and inventory optimization. Knowledge of Python for data analysis is beneficial.'
    },
    
    # Kimley-Horn
    {
        'company': 'Kimley-Horn',
        'title': 'Transportation Engineer',
        'description': 'Design roadway and traffic systems using AutoCAD Civil 3D and Synchro. Knowledge of traffic simulation, transportation planning, and FDOT/AASHTO standards. Strong technical writing and client communication skills. EIT certification required, PE preferred.'
    },
    {
        'company': 'Kimley-Horn',
        'title': 'Structural Engineer',
        'description': 'Design commercial and residential structures using SAP2000, ETABS, or RISA. Strong knowledge of structural analysis, building codes (IBC, ASCE 7), and construction materials. Proficiency in AutoCAD and Revit. EIT required, SE license path preferred.'
    },
    
    # LJA Engineering
    {
        'company': 'LJA Engineering',
        'title': 'Land Development Engineer',
        'description': 'Design site development projects using Civil 3D and StormCAD. Knowledge of grading, drainage design, and local development regulations. Strong coordination skills with architects, surveyors, and contractors. Experience with permitting and construction administration.'
    },
    {
        'company': 'LJA Engineering',
        'title': 'Survey Technician',
        'description': 'Perform field surveys and process data using Trimble and Leica equipment. Knowledge of boundary surveys, topographic mapping, and construction staking. Proficiency in AutoCAD, Civil 3D, and survey data processing software. Strong attention to detail and teamwork skills.'
    },
    
    # P&G
    {
        'company': 'Procter & Gamble',
        'title': 'Process Engineer - Manufacturing',
        'description': 'Improve manufacturing processes in consumer goods production. Strong knowledge of process optimization, Six Sigma, and Lean methodologies. Experience with automation, PLC programming, and data analysis. Proficiency in Python, SQL, and statistical software like Minitab.'
    },
    {
        'company': 'Procter & Gamble',
        'title': 'Product Development Engineer',
        'description': 'Design and test new consumer products. Knowledge of materials science, product formulation, and quality control. Experience with CAD software, prototyping, and lab testing. Strong project management and cross-functional collaboration skills required.'
    },
    
    # Trinity Consultants
    {
        'company': 'Trinity Consultants',
        'title': 'Air Quality Engineer',
        'description': 'Conduct air quality modeling and permitting using AERMOD and EPA regulations. Knowledge of emissions calculations, dispersion modeling, and environmental compliance. Strong technical writing and client interaction skills. Experience with GIS and data analysis tools.'
    },
    {
        'company': 'Trinity Consultants',
        'title': 'Environmental Consultant',
        'description': 'Provide environmental compliance consulting services. Knowledge of NEPA, Clean Air Act, and Clean Water Act regulations. Experience with environmental assessments, remediation design, and sustainability planning. Strong analytical and communication skills required.'
    },
    
    # Whiting-Turner
    {
        'company': 'Whiting-Turner',
        'title': 'Construction Project Engineer',
        'description': 'Manage construction projects from planning to completion. Knowledge of building codes, construction methods, and project scheduling using Primavera P6 or Microsoft Project. Strong skills in Bluebeam, AutoCAD, and Procore. Excellent communication and problem-solving abilities.'
    },
    {
        'company': 'Whiting-Turner',
        'title': 'Estimator',
        'description': 'Prepare cost estimates for construction projects. Experience with quantity takeoffs, cost analysis, and bid preparation. Proficiency in Excel, construction estimating software, and reading blueprints. Strong attention to detail and knowledge of construction materials and methods.'
    },
    
    # Disney
    {
        'company': 'Disney',
        'title': 'Software Engineer - Streaming',
        'description': 'Develop streaming video applications using JavaScript, React, and Node.js. Experience with video encoding, CDN technologies, and cloud platforms (AWS, Azure). Knowledge of performance optimization, microservices, and API development. Strong problem-solving skills required.'
    },
    {
        'company': 'Disney',
        'title': 'Mechanical Engineer - Theme Parks',
        'description': 'Design and maintain ride systems and attractions. Strong knowledge of mechanical systems, hydraulics, and controls. Experience with SolidWorks, FEA, and safety systems. Understanding of show control systems and project management. Creative problem-solving skills essential.'
    },
    
    # JP Morgan
    {
        'company': 'JP Morgan Chase',
        'title': 'Quantitative Analyst',
        'description': 'Develop quantitative models for trading and risk management. Strong skills in Python, R, C++, and financial mathematics. Knowledge of statistics, machine learning, and optimization algorithms. Experience with SQL, big data technologies, and financial markets.'
    },
    {
        'company': 'JP Morgan Chase',
        'title': 'Software Engineer - Backend',
        'description': 'Build scalable backend services using Java, Spring Boot, and microservices architecture. Experience with distributed systems, SQL/NoSQL databases, and cloud platforms. Strong knowledge of algorithms, data structures, and system design. Agile development experience required.'
    },
    
    # Jane Street
    {
        'company': 'Jane Street',
        'title': 'Software Engineer - Trading Systems',
        'description': 'Develop high-performance trading systems using OCaml, Python, or C++. Strong knowledge of algorithms, data structures, and functional programming. Experience with low-latency systems, distributed computing, and real-time data processing. Excellent problem-solving skills required.'
    },
    {
        'company': 'Jane Street',
        'title': 'Quantitative Trader',
        'description': 'Design and implement trading strategies using quantitative methods. Strong skills in mathematics, statistics, and programming (Python, R, or OCaml). Knowledge of financial markets, probability theory, and machine learning. Excellent analytical and decision-making abilities.'
    },
    
    # Microsoft
    {
        'company': 'Microsoft',
        'title': 'Software Engineer - Cloud Services',
        'description': 'Build cloud infrastructure and services on Azure. Strong programming skills in C#, Python, or Java. Experience with distributed systems, microservices, and DevOps. Knowledge of Kubernetes, Docker, and CI/CD pipelines. Strong system design and problem-solving abilities.'
    },
    {
        'company': 'Microsoft',
        'title': 'Data Scientist',
        'description': 'Develop machine learning models and analytics solutions. Strong skills in Python, R, TensorFlow, and PyTorch. Experience with statistical analysis, deep learning, and big data tools (Spark, Hadoop). Knowledge of Azure ML, SQL, and data visualization. Excellent communication skills.'
    },
    
    # Texas Instruments
    {
        'company': 'Texas Instruments',
        'title': 'Embedded Software Engineer',
        'description': 'Develop embedded software for microcontrollers and processors. Strong proficiency in C and C++ with experience in RTOS (FreeRTOS, VxWorks). Knowledge of ARM architecture, device drivers, and hardware interfaces (I2C, SPI, UART). Experience with debugging tools, oscilloscopes, and version control (Git).'
    },
    {
        'company': 'Texas Instruments',
        'title': 'Analog Design Engineer',
        'description': 'Design analog and mixed-signal integrated circuits. Strong knowledge of circuit design, transistor-level design, and layout. Experience with Cadence tools, SPICE simulation, and semiconductor physics. Understanding of signal processing, amplifiers, and data converters. MSEE preferred.'
    },
]


def scrape_all_job_data(use_test_data=True):
    """
    Scrapes job data from SHPE sponsor companies.
    
    Args:
        use_test_data (bool): If True, returns test data instead of scraping
        
    Returns:
        list: List of job dictionaries with 'company', 'title', and 'description'
    """
    if use_test_data:
        return SHPE_COMPANY_JOBS
    
    # TODO: Implement actual web scraping logic here
    # This would involve using BeautifulSoup, Selenium, or API calls
    # to scrape real job postings from company websites
    
    jobs = []
    # Your scraping logic would go here
    return jobs


def scrape_company_jobs(company_name, use_test_data=True):
    """
    Scrapes jobs from a specific company.
    
    Args:
        company_name (str): Name of the company to scrape
        use_test_data (bool): If True, returns test data for that company
        
    Returns:
        list: List of job dictionaries for the specified company
    """
    if use_test_data:
        return [job for job in SHPE_COMPANY_JOBS if job['company'] == company_name]
    
    # TODO: Implement company-specific scraping
    jobs = []
    return jobs``