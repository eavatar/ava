The working directory for the agent.

The directory structure:
├── conf              -- configuration files
├── data              -- data folder
├── logs              -- log files
├── mods              
│   ├── available     -- available modules
│   └── enabled       -- enabled modules
├── pkgs              -- extension packages
└── static            -- static web resources such ico, images, css, etc.

__init__.py is to make pod folder be a valid package so that the structure is 
maintained.