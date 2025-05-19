# Munchbot – Your AI-Powered Calorie Tracking Assistant

Munchbot is your personal AI nutrition assistant designed to help you track meals, set personalized goals, and stay on top of your health journey — all in one smart, intuitive interface.

---

## What Munchbot Does

- Chat with Munchbot to log meals and ask food-related queries.
- Set and track goals for calories, protein, carbs, fats, and sugars.
- Visualize your daily intake and nutrition trends.
- Manage your nutrition profile and preferences.

---

## Tech Stack

- **FastAPI** – Backend API framework
- **Pydantic-AI** – Schema-driven integration of AI into chat memory
- **Redis** – In-memory store for caching, rate limits, and sessions
- **Alembic** – Database migrations and schema version control
- **Uvicorn** – ASGI server for async FastAPI performance
- **PostgreSQL** – Persistent relational user data
- **Docker** – Containerization for cloud deployment
- **GCP Cloud Run** – Scalable backend hosting
- **Next.js** – React-based frontend framework
- **ShadCN UI** – Accessible and beautiful UI components
- **V0.dev** – AI-assisted UI builder for Tailwind + ShadCN prototyping

---

##  Screenshots

[Find screenshots here »](https://github.com/rohanrjp/MunchBot-Backend/issues/21#issue-3074839668)

---

## Lessons Learned

Building Munchbot was a deep learning experience. Some of the major takeaways:

### 🔷 Pydantic-AI
- Used strongly typed Pydantic models to structure AI inputs/outputs.
- Reduced bugs caused by unpredictable LLM responses.

### 🔷 FastAPI + AsyncIO + Background Tasks
- Leveraged async endpoints to keep APIs responsive.
- Offloaded long-running tasks (like AI response generation) using `background_tasks`.
- Understood the critical role of non-blocking I/O in production APIs.

### 🔷 Uvicorn & ASGI
- Used Uvicorn to serve FastAPI with native async support.
- Learned about lifespan event hooks and concurrency issues during cold starts.

### 🔷 Alembic for Database Migrations
- Adopted Alembic for clean, versioned schema migrations.
- Made it easy to collaborate with DB schema changes across environments.

### 🔷 Redis Integration
- Used Redis for:
  - Caching nutrition metadata
  - Session and rate-limit token management
  - Speeding up common requests
- Learned about expiration policies and memory-safe caching strategies.

### 🔷 CORS & Cloud Hosting Challenges
- Debugged CORS issues, especially around `Authorization` headers.
- Fixed via `allow_credentials=True` and specifying `allow_origins`.

### 🔷 Mobile UX Debugging
- Identified mobile-only sidebar issues related to z-index and pointer-events.
- Reinforced the importance of multi-device testing.

### 🔷 Auth Flow & Cold Start Fixes
- Cloud Run cold starts caused login requests to fail initially.
- Improved error messaging and considered pre-warming strategies to mitigate.

---

## Demo

[Try Munchbot →](https://v0-sidebar-12-ashy.vercel.app/)

---

## Roadmap

- [ ] Integrate LangGraph for better AI agent orchestration
- [ ] Add Google OAuth for smooth onboarding
- [ ] Implement a payment gateway
- [ ] Launch a premium coaching tier with weekly feedback and analytics

---

## Author

- [@rohanrjp](https://github.com/rohanrjp)

---

## Contributing

This is a closed-source product. If you're interested in collaborating:

- 📧 Email: rohan1007rjp@gmail.com
- 🐛 Open an issue for bug reports, ideas, or feedback

---

## License

This project is not open-source. All rights reserved © [Rohan Paul], 2025.