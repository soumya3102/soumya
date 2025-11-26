💡 Sankalp Sarathi: Multi-Agent System for Government Scheme Empowerment

**Project Status:** Implemented and Deployed (Sequential Multi-Agent System)

## 🎯 I. Problem Statement & Value Proposition

India's vast network of social welfare schemes (*Yojanas*) often fails to reach its intended low-income and rural beneficiaries due to **fragmented information**, **complex legalistic eligibility criteria**, and **high application friction**.

**Sankalp Sarathi** solves this by creating a **citizen-centric, hyper-personalized guidance system** that breaks down these barriers. It's an **Agents for Good** project focused on:

  * **Accessibility:** Providing guidance in local context/language.
  * **Efficiency:** Automating eligibility analysis and document preparation.
  * **Empowerment:** Ensuring citizens receive the welfare support they are entitled to.

-----

## 🤖 II. Why Agents? The Architecture Rationale

The end-to-end task—from identifying the user's need to generating an application guide—requires distinct, specialized cognitive steps. This is optimally handled by a **Sequential Multi-Agent System (MAS)** rather than a single large LLM prompt.

| Agent Name | Role / Function | Cognitive Task | Primary Model |
| :--- | :--- | :--- | :--- |
| **1. Orchestrator Agent (The Guide)** | Manages the session and delegates the workflow sequentially. | **Delegation & Session Management** | Gemini 2.5 Flash |
| **2. Eligibility Agent (The Analyst)** | Determines precise eligibility by checking user profile against scheme criteria. | **Complex Reasoning & Tool Use** | **Gemini 2.5 Pro** |
| **3. Document Agent (The Preparer)** | Generates the final, actionable checklist and finds application links. | **Synthesis & External Tool Simulation** | Gemini 2.5 Flash |

### Agent Flow:

<img width="713" height="501" alt="Screenshot (645)" src="https://github.com/user-attachments/assets/7b0785e0-ebc1-4b3f-9a36-10a654d724b5" />

1.  **User Query** $\rightarrow$ **Orchestrator** (fetches profile from **Memory Bank**).
2.  **Orchestrator** delegates $\rightarrow$ **Eligibility Agent**.
3.  **Eligibility Agent** calls **Custom Tool (Scheme DB)** $\rightarrow$ Applies **Context Compaction** $\rightarrow$ Analyzes with **Gemini Pro**.
4.  **Eligibility Agent** passes results $\rightarrow$ **Document Agent**.
5.  **Document Agent** generates guide using **Built-in Tool** simulation and **A2A Protocol** status.


-----

## 🛠️ III. Technical Implementation & Core Concepts

The project utilizes the Gemini API to implement the required technical concepts across its modular file structure.

| Technical Concept | Implementation Detail | Location in Code |
| :--- | :--- | :--- |
| **Effective Use of Gemini** | Uses `gemini-2.5-pro` for high-accuracy eligibility analysis and `gemini-2.5-flash` for conversational flow/guide generation. | `config.py`, `agents/*` |
| **Multi-Agent System** | Sequential delegation of tasks managed by the Orchestrator agent. | `agents/orchestrator.py` |
| **Custom Tool** | **`SchemeDBConnector`** simulates RAG by retrieving structured scheme data based on the query topic. | `tools/scheme_db_connector.py` |
| **Sessions & Memory** | `InMemorySessionService` manages the active conversation. **Memory Bank** stores the static `user_profile` to prevent repetitive questioning. | `utils/memory.py` |
| **Context Engineering** | **`context_compaction`** function filters raw RAG output using the user profile before passing it to the LLM, reducing noise and tokens. | `utils/context_engine.py` |
| **Built-in Tools** | **Google Search** is simulated by the Document Agent to find real-time application links. | `agents/document_agent.py` |
| **A2A Protocol** | Simulated check against the user's 'Digital Locker' to pre-verify documents, generating the `A2A Protocol Status`. | `agents/document_agent.py` |

-----

## 📹 IV. Demo: Dinesh Kumar's Session

This demo showcases Dinesh Kumar, a farmer in Bihar, seeking assistance after crop failure.

**User Input (Translated):** "My crop has failed. I am a farmer in Bihar. Is any government help available?"

### **Behind the Scenes Flow:**

| Agent Action | Output/Status |
| :--- | :--- |
| **Orchestrator** | Fetches Dinesh's profile (Farmer, Bihar, Income ₹70k). |
| **Eligibility Agent** | Runs **Custom Tool** (RAG search for "crop failure, farmer"). |
| **Eligibility Agent** | **Gemini Pro** analyzes and confirms eligibility for both **PMKY (Central)** and **BFRY (Bihar)** based on income/state criteria. |
| **Document Agent** | Simulates **Google Search** for application links and reviews document requirements. |

### **Final Output:**

```markdown
=======================================================
                FINAL APPLICATION GUIDE
=======================================================
✅ **Summary:** You are eligible for the Central Pradhan Mantri Kisan Yojana and the state's Bihar Fasal Rahat Yojana.

## 📝 Personalized Application Checklist

1.  **Aadhar Card:** (Verified via A2A Protocol)
2.  **Land Ownership Proof:** (Verified via A2A Protocol)
3.  **Bank Passbook:** (Required for subsidy transfer)
4.  **Crop Damage Report:** (⚠️ **ACTION NEEDED:** Must be obtained from the local agriculture office)

## 🔗 Application Links (Simulated Google Search)

* **Pradhan Mantri Kisan Yojana:** [http://simulated-pmky-official-portal.gov.in/apply]
* **Bihar Fasal Rahat Yojana:** [http://simulated-bfry-online-form.bih.nic.in]

### A2A Protocol Status
✅ **A2A Protocol Status:** Digital Locker check is complete. Your Aadhar Card and Land Records are pre-verified and ready for submission.
```

-----

## 🚀 V. Setup, Execution, and Future Scope

### Setup and Execution

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/soumya3102/soumya.git sankalp_sarathi
    cd sankalp_sarathi
    ```
2.  **Install Dependencies & Key:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    # Ensure .env file contains GEMINI_API_KEY="YOUR_KEY_HERE"
    ```
3.  **Run the Multi-Agent System:**
    ```bash
    python main.py
    ```

### If I Had More Time, I Would...

1.  **Loop Agent Structure:** Refactor the sequential flow into a **Loop Agent** (e.g., using LangGraph) to implement **remediation**. If the Document Agent flags a missing document, the Orchestrator would enter a loop to prompt the user to upload it before proceeding.
2.  **Multimodal Voice Input:** Integrate ASR (Automatic Speech Recognition) to allow voice queries in regional languages, dramatically improving accessibility for low-literacy rural users.
3.  **Cloud Deployment:** Deploy the agents as a scalable, live service using **Cloud Run** or similar containerization to handle high user loads.
