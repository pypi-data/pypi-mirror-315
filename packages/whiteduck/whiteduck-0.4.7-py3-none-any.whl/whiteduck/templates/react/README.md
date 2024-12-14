# Project Starter with React Frontend 🚀

![image](https://github.com/user-attachments/assets/bba4737e-5b20-441e-9089-5e99f5d965e6)

A modern project template featuring a React frontend with Python backend integration.

## Prerequisites

### UV Package Manager

This project uses [UV](https://github.com/astral-sh/uv), a modern Python package manager.

#### Installation

Visit the official documentation for detailed installation instructions:
- [UV Installation Guide](https://docs.astral.sh/uv/)
- [UV GitHub Repository](https://github.com/astral-sh/uv)

## 🛠 Setup & Development

### Initial Setup

Synchronize all project dependencies:
```bash
uv sync --all-groups
```

### Available Commands

#### Full Stack Development
Run both frontend and backend (recommended for development):
```bash
uv run poe run
```
This command will:
- Build the frontend
- Start the Python backend
- Serve the frontend through the backend server

#### Frontend Only

Build the frontend:
```bash
uv run poe build_frontend
```

Start the frontend development server:
```bash
uv run poe run_frontend
```
This will serve the frontend using Vite's development server with hot module replacement.

## 📦 Project Structure

- `/src/frontend` - React frontend application
- `/src/myproject` - Python backend application

## 🔧 Technology Stack

- **Frontend**: React + TypeScript + Vite
- **Backend**: Python
- **Package Management**: UV
- **Task Runner**: Poethepoet (poe)
