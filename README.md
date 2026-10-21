# chatbot-security-assessment
Final year project for BSc (Hons) Computer Science for Cyber Security: OWASP-based security testing of a Rasa chatbot (injection, access control, misconfiguration, cryptographic failures.

I built a hotel-booking chatbot with the open-source Rasa framework and then tested it against four categories from the OWASP Top 10: SQL injection, broken access control, security misconfiguration and cryptographic failures. The full write-up can be found in the report document.

 # Contents:
. Overview
. Repository structure
. The chatbot
. Security testing
. Key findings
. Limitations
. Future work
. Running the project
. Skills demonstrated
. Ethics
. Author
. Overview

Chatbots are now widely used in healthcare, finance and customer service, which makes them an attractive target for attackers. This project looks at how a chatbot built on Rasa holds up against common web and API attacks, and recommends ways developers can make their chatbots more secure.

# What I did:

Researched chatbot architecture, common vulnerabilities, and the legal and ethical issues around chatbots (including GDPR and HIPAA).
Built a working Rasa chatbot with login, role-based access and booking features to act as the test target.
Designed and ran penetration tests based on the OWASP Top 10, using manual curl requests and network capture.
Documented the results and wrote recommendations for improving chatbot security.


# Repository structure
.
├── README.md
├── report/                      Final project report (DOC)
├── chatbot/                     Rasa chatbot used as the test target
│   ├── actions/
│   │   └── actions.py           Custom actions: login, booking, cancelling, privilege checks
│   ├── data/
│   │   ├── nlu.yml              Intents and training examples
│   │   ├── stories.yml          Conversation flows
│   │   └── rules.yml            Fixed responses to specific intents
│   ├── domain.yml               Intents, responses, slots and actions
│   ├── config.yml               NLU pipeline and policies
│   ├── credentials.yml          Channel settings (no secrets)
│   └── endpoints.yml            Action server endpoint
└── tests/                       Test tables and screenshots
The chatbot

A simple hotel-booking assistant. Users can log in, book a room and cancel their booking, and there are two roles: user and admin.

All data is held in in-memory Python dictionaries, so there is no real database.
Every username and password in actions.py is a made-up demo credential for testing only.
Custom behaviour is written in Python (actions.py), and the conversation design lives in the Rasa YAML files.
Security testing

OWASP category	What I tested	Outcome:
. Injection	SQL-injection-style payloads sent through the chat and directly to the REST webhook with curl	Payloads were not executed; the bot asked the user to log in
. Broken access control -	A regular user trying admin actions, cancelling another user's booking, and calling the API directly	Requests were denied
. Security misconfiguration -	Invalid payloads, admin tracker and debug endpoints, CORS behaviour, error handling	Access denied; responses stayed generic
. Cryptographic failures -	Network traffic inspection with tcpdump, path traversal attempts, manipulated tokens, review of password storage	No sensitive data  exposed in the tests; password hashing flagged as weak

Each test case is written up with its command, expected result and actual result in Chapter 4 of the report.

# Key findings:
. The chatbot rejected the injection payloads and kept asking for authentication rather than executing them.
. Role checks prevented a normal user from cancelling the admin's booking or reaching admin-only endpoints.
. Debug and admin endpoints were not exposed, and unusual requests produced generic responses.
. Password storage was the weakest area, and the report recommends stronger hashing.

These results apply to a small demo system. They show how a basic Rasa bot behaves under these specific tests.

# Limitations:

This is a deliberately simple system, so the results do not prove that Rasa applications are secure in general. Things I would improve in a real deployment:

. Password hashing: the demo uses unsalted MD5. A real system should use a slow, salted algorithm such as bcrypt or Argon2.
. Access control: the check that stops a user cancelling another user's booking looks for keywords in the message. A real system should use proper identity and session checks instead of text matching.
. Authentication state: login state is kept in conversation slots, with no real session management or multi-factor authentication.
. Test scope: only four of the OWASP Top 10 categories were covered.

# Future work:
Add the remaining categories, such as authentication failures and security logging and monitoring failures.
Test for cross-site scripting, social engineering and prompt injection in LLM-based chatbots.
Automate scanning with OWASP ZAP and compare the results with the manual tests.
Explore intrusion detection and multi-factor authentication for chatbot platforms.


# Running the project
1. Install Python and Rasa (see the Rasa docs for the version that matches your Python).
2. Open a terminal in the chatbot folder and train the model:
   rasa train
3. Start the custom action server in one terminal:
   rasa run actions
4. Start the chatbot in a second terminal:
   rasa shell

   
# Skills demonstrated:
. Penetration testing, OWASP Top 10, vulnerability assessment, API security testing, Python, Rasa (NLU, stories, rules, custom actions), curl, tcpdump, access control and authentication concepts, security reporting and technical writing.

# Ethics:

All testing was carried out against my own chatbot running on my own machine. No third-party systems, real user data or real credentials were used.

Author

Abdullah Sajjad 
