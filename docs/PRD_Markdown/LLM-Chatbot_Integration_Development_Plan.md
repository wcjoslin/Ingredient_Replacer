<create_file>
<path>PRD_Markdown/LLM_Chatbot_Integration_Development_Plan.md</path>
<content>
# LLM Chatbot Integration Development Plan

## Overview

Integrate an LLM-powered chatbot into the Ingredient Replacer landing page. The chatbot will allow users to interactively ask questions about recipes, diet restrictions, and ingredient swaps, and will provide context-aware responses based on the app’s capabilities.

---

## 1. UI Architecture

- **Location:** `app-landing-page/src/app/page.tsx`
- **Features:**
  - Add a chat window component below or beside the recipe entry bar.
  - Chat window expands vertically as messages are added (ChatGPT-style).
  - Each message (user or bot) is rendered as a chat bubble.
  - Input bar with placeholder: “Enter your recipe or question here…”
  - Accepts both recipe URLs and plain text questions.
  - On submit, message is appended to chat history and sent to backend.

---

## 2. Backend API Planning

- **Endpoint:** `app-landing-page/src/app/api/chat.ts`
- **Request:**
  - `messages`: Array of chat history objects `{role: "user"|"assistant", content: string}`
  - `context`: Optional string for app context (capabilities, files, etc.)
- **Response:**
  - `reply`: LLM-generated response string

- **LLM Provider Integration:**
  - Use OpenAI’s GPT-3.5/4 API via `openai` npm package.
  - Store API key securely (environment variable).

- **Context Injection:**
  - Prepend system prompt to messages:
    - Example: “You are the Ingredient Replacer app assistant. You can analyze recipes, suggest ingredient swaps, and answer diet questions. You have access to ingredient data and recipe analysis tools.”
  - Optionally inject relevant file or capability context from the backend.

- **Recipe URL and Question Handling:**
  - If user input is a URL, parse and extract recipe data (reuse logic from `scrape.ts`).
  - Pass extracted recipe info as part of the context to the LLM.

- **Ingredient Filtering Logic:**
  - Optionally add middleware to detect ingredient/diet queries and enrich the prompt/context before sending to LLM.

- **Response Handling:**
  - Return the LLM’s reply to the frontend for display in the chat UI.

- **Security & Rate Limiting:**
  - Implement basic rate limiting and input validation to prevent abuse.

---

## 3. Example API Handler Skeleton (`chat.ts`)

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { OpenAI } from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function POST(req: NextRequest) {
  const { messages, context } = await req.json();

  const systemPrompt = context || "You are the Ingredient Replacer app assistant. ...";
  const chatMessages = [
    { role: "system", content: systemPrompt },
    ...messages
  ];

  const completion = await openai.chat.completions.create({
    model: "gpt-4",
    messages: chatMessages,
    max_tokens: 512,
    temperature: 0.7,
  });

  return NextResponse.json({ reply: completion.choices[0].message.content });
}
```

---

## 4. Development Steps

1. **Frontend Implementation**
    - Update landing page React components to add chat UI.
    - Implement expandable chat window and chat bubbles.
    - Connect chat input to backend API.

2. **Backend Implementation**
    - Create/extend API endpoint for LLM chat.
    - Integrate with chosen LLM provider.
    - Pass relevant app context to LLM (files, capabilities).
    - Handle recipe URL parsing and context injection.

3. **Testing & Acceptance**
    - Test user stories: general questions, diet restrictions, recipe analysis.
    - Validate chat context and filtering logic.
    - Ensure UI/UX matches acceptance criteria.

4. **Documentation**
    - Update README and PRD with integration details and usage instructions.

---

## 5. Acceptance Criteria

- Chatbot integration into application.
- Chatbot/LLM has context of the files and capabilities of the app.
- User is able to enter plain text questions and recipe URLs to get an understanding of their recipe and how it works with their diet.

---

## 6. User Stories

- As a user I want to use a chatbot to understand what an app can do for me.
- As a user I want to ask questions about diet restrictions so I can choose the right diet for me in the app.
- As a user I want to understand what parts of a recipe may be changed in my recipe before I ask for swap suggestions.

</content>
