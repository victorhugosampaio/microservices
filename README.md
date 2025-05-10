# 🧩 E-commerce SPL - Software Product Line with Microservices

This project implements a **Software Product Line (SPL)** for a modular e-commerce system based on a **microservices architecture**. Each core feature of the system (catalog, cart, shipping, payment, purchase, and user management) is implemented as an independent microservice, each with its own graphical user interface (GUI) developed in Python using Tkinter.

## 🎯 Objective
Demonstrate the practical application of Software Product Line Engineering (SPLE) concepts in a distributed and reusable microservices architecture, allowing easy customization and evolution of features according to product needs.

## 🔧 Implemented Microservices
- **Product Catalog** (`catalog`)
- **Shopping Cart** (`cart`)
- **Shipping Service** (`shipping`)
- **Payment System** (`payments`)
- **Purchase Finalization** (`purchase`)
- **User Management** (`user`)

## 🖥️ Graphical Interface
Each microservice includes its own GUI, allowing individual use or integration within a unified environment managed by the main interface (`main_gui`).

## 📦 Features
- Communication between microservices through data exchange and database access.
- Independent MySQL database for each microservice.
- Full CRUD operations in each service.
- Tab-based navigation between services.
- Modular customization oriented toward reuse.

## 🚀 Technologies
- Python 3
- Tkinter (GUI)
- MySQL
- Microservices architecture
- SPLE (Software Product Line Engineering)

## 🛠️ Setup Instructions
1. Install [MySQL](https://www.mysql.com/) and create the required databases.
2. Install Python dependencies (if any).
3. Run the system with:

```bash
python .\FeatureSelector.py (choose the desired microservices then type done to save and exit)
python .\FeatureSelector.py --generate (to generate the microservices)
python .\start_services.py (start the microservices services)
cd build (change directory to build folder)
python gui.py (open GUI)
```

Each microservice GUI will be loaded as a tab.

---

Developed for academic purposes to demonstrate SPL and microservices integration in a GUI-based e-commerce system.