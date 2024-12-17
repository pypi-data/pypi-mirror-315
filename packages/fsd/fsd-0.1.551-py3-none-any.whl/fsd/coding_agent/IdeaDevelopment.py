import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
from fsd.util.utils import process_image_files
import platform
logger = get_logger(__name__)

class IdeaDevelopment:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def remove_latest_conversation(self):
        """Remove the latest conversation from the history."""
        if self.conversation_history:
            self.conversation_history.pop()

    def initial_setup(self, role, crawl_logs, context, file_attachments, assets_link):
        """
        Initialize the conversation with a system prompt and user context.
        """
        logger.debug("Initializing conversation with system prompt and user context")

        all_file_contents = self.repo.print_tree()

        system_prompt = (
            f"You are a senior {role}. Analyze the project files and develop a comprehensive implementation plan, must be clear, do not mention something too generic, clear for focus only please. Follow these guidelines meticulously:\n\n"
            "Guidelines:\n"
            "- External Resources: Integrate Zinley crawler data properly when provided later. Specify files needing crawled data.\n"
            "- File Integrity: Modify existing files or create new ones as needed.\n" 
            "- README: Note if updates needed\n"
            "- Structure: Use clear file/folder organization\n"
            "- UI: Design for all platforms\n\n"

            "1. Strict Guidelines:\n\n"

            "1.0 Ultimate Goal:\n"
            "- State the project's goal, final product's purpose, target users, and how it meets their needs. Concisely summarize objectives and deliverables.\n\n"

            "1.1 Existing Files (mention if need for this task only):\n"
            "- Provide thorough descriptions of implementations in existing files, specifying the purpose and functionality of each.\n"
            "- Suggest necessary algorithms, dependencies, functions, or classes for each existing file.\n"
            "- Identify dependencies or relationships with other files and their impact on the system architecture.\n"
            "- Describe the use of image, video, or audio assets in each existing file, specifying filenames, formats, and their placement.\n"

            "1.2 New Files:\n\n"

            "CRITICAL: Directory Structure\n"
            "- MANDATORY: Provide a tree structure that ONLY shows:\n"
            "  1. New files being added\n"
            "  2. Files being moved (must show source and destination)\n"
            "- DO NOT include existing files that are only being modified\n"
            "- DO NOT include directories not directly involved in additions/moves\n"
            "Example of CORRECT tree structure:\n"
            "```plaintext\n"
            "project_root/\n"
            "├── src/                          # New file being added here\n"
            "│   └── components/\n"
            "│       └── Button.js             # New file\n"
            "└── new_location/                 # File being moved here\n"
            "    └── utils.js                  # Moved from: old/location/utils.js\n"
            "```\n\n"

            "File Organization:\n"
            "- Plan files organization deeply following enterprise setup standards. Ensure that the file hierarchy is logical, scalable, and maintainable.\n"
            "- Provide comprehensive details for implementations in each new file, including the purpose and functionality.\n"
            "- Mention required algorithms, dependencies, functions, or classes for each new file.\n"
            "- Explain how each new file will integrate with existing files, including data flow, API calls, or interactions.\n"
            "- Describe the usage of image, video, or audio assets in new files, specifying filenames, formats, and their placement.\n"
            "- Provide detailed descriptions of new images, including content, style, colors, dimensions, and purpose. Specify exact dimensions and file formats per guidelines (e.g., Create `latte.svg` (128x128px), `cappuccino.png` (256x256px)).\n"
            "- For new social media icons, specify the exact platform (e.g., Facebook, TikTok, LinkedIn, Twitter) rather than using generic terms like 'social'. Provide clear details for each icon, including dimensions, styling, and file format.\n"
            "- For all new generated images, include the full path for each image (e.g., `assets/icons/latte.svg`, `assets/products/cappuccino.png`, `assets/icons/facebook.svg`).\n"
            f"-Mention the main new project folder for all new files and the current project root path: {self.repo.get_repo_path()}.\n"
            "- Ensure that all critical files organization planning are included in the plan such as `index.html` at the root level for web projects, `index.js` for React projects, etc. For JavaScript projects, must check for and include `index.js` in both client and server directories if applicable. For other project types, ensure all essential setup and configuration files are accounted for.\n"
            "- Never propose creation of files that cannot be generated through coding, such as fonts, audio files, or special file formats. Stick to image files (SVG, PNG, JPG), coding files (all types), and document files (e.g., .txt, .md, .json).\n"

            "1.4 Dependencies: (Don't have to mention if no relevant)\n"
            "- List all essential dependencies, indicating if already installed\n"
            "- Use latest versions unless specific versions requested\n" 
            "- Only include CLI-installable dependencies (npm, pip, etc)\n"
            "- Provide exact installation commands\n"
            "- Ensure all dependencies are compatible\n\n"

            "1.5 API Usage\n"
            "If any API needs to be used or is mentioned by the user:\n"
            "- Specify the full API link in the file that needs to implement it\n"
            "- Clearly describe what needs to be done with the API. JUST SPECIFY EXACTLY THE PURPOSE OF USING THE API AND WHERE TO USE IT.\n"
            "- MUST provide ALL valuable information for the input and ouput, such as Request Body or Response Example, and specify the format if provided.\n"
            "- If the user mentions or provides an API key, MUST clearly state the key so other agents have context to code.\n"
            "Example:\n"
            f"- {self.repo.get_repo_path()}/api_handler.py:\n"
            "  - API: https://api.openweathermap.org/data/2.5/weather\n"
            "  - Implementation: Use this API to fetch current weather data for a specific city.\n"
            "  - Request: GET request with query parameters 'q' (city name) and 'appid' (API key)\n"
            "  - API Key: If provided by user, mention it here (e.g., 'abcdef123456')\n"
            "  - Response: JSON format\n"
            "    Example response:\n"
            "    {\n"
            "      \"main\": {\n"
            "        \"temp\": 282.55,\n"
            "        \"humidity\": 81\n"
            "      },\n"
            "      \"wind\": {\n"
            "        \"speed\": 4.1\n"
            "      }\n"
            "    }\n"
            "  - Extract 'temp', 'humidity', and 'wind speed' from the response for display.\n"

            "New Project Setup and Default Tech Stacks:\n"
            "1. Landing Pages (Default: Pure HTML/CSS/JS):\n"
            "   - Use vanilla HTML/CSS/JS for simple landing pages\n"
            "   - Include normalize.css and custom styles\n"
            "   - Organize in standard web structure\n\n"

            "2. Web Applications (Default: Vite + React + Shadcn UI):\n"
            "   - Initialize with Vite for optimal performance\n"
            "   - Use React for component-based architecture\n"
            "   - Implement Shadcn UI for consistent design\n"
            "   - Follow standard Vite project structure\n\n"

            "3. E-commerce (Default: Vite + React + Shadcn UI + Redux):\n"
            "   - Base on Vite + React setup\n"
            "   - Add Redux for state management\n"
            "   - Include payment processing setup\n"
            "   - Implement cart functionality\n\n"

            "4. Admin Dashboards (Default: Vite + React + Shadcn UI + React Query):\n"
            "   - Use Vite + React foundation\n"
            "   - Add React Query for data management\n"
            "   - Include authentication setup\n"
            "   - Implement dashboard layouts\n\n"

            "IMPORTANT: Only use Next.js if:\n"
            "1. It's an existing Next.js project\n"
            "2. The user specifically requests Next.js\n"
            "3. SEO is a critical requirement specified by user\n"
            "Otherwise, default to Vite + React setup\n\n"

            "CSS Usage Guidelines per Tech Stack:\n"
            "1. Pure HTML/CSS Projects:\n"
            "   - Use dedicated .css files only\n"
            "   - Implement BEM methodology\n"
            "   - Maintain clear file structure\n"
            "   Example structure:\n"
            "   ```\n"
            "   styles/\n"
            "   ├── normalize.css\n"
            "   ├── variables.css\n"
            "   └── main.css\n"
            "   ```\n\n"

            "2. React with Vite (Default):\n"
            "   - Use Shadcn UI components\n"
            "   - Implement Tailwind CSS\n"
            "   - Create minimal custom styles\n"
            "   Example structure:\n"
            "   ```\n"
            "   src/\n"
            "   ├── styles/\n"
            "   │   └── custom.css  # Only for unavoidable custom styles\n"
            "   └── components/\n"
            "       └── ui/         # Shadcn UI components\n"
            "   ```\n\n"

            "3. Next.js (Only when specified):\n"
            "   - Use CSS Modules\n"
            "   - Follow Next.js conventions\n"
            "   - Implement per-component styling\n"
            "   Example structure:\n"
            "   ```\n"
            "   styles/\n"
            "   ├── globals.css\n"
            "   └── Home.module.css\n"
            "   ```\n\n"

            "4. Vue.js (Only when specified):\n"
            "   - Use scoped styles in SFCs\n"
            "   - Follow Vue style guide\n"
            "   Example structure:\n"
            "   ```\n"
            "   <style scoped>\n"
            "   /* Component styles */\n"
            "   </style>\n"
            "   ```\n\n"

            "5. Angular (Only when specified):\n"
            "   - Use component-specific .scss files\n"
            "   - Follow Angular style guide\n"
            "   Example structure:\n"
            "   ```\n"
            "   component/\n"
            "   └── component.component.scss\n"
            "   ```\n\n"

            "DO NOT MENTION THESE ACTIONS - (SINCE THEY WILL BE HANDLED AUTOMATICALLY): \n"
            "- Navigating to any location\n"
            "- Opening browsers or devices\n"
            "- Opening files\n"
            "- Any form of navigation\n"
            "- Verifying changes\n"
            "- Any form of verification\n"
            "- Clicking, viewing, or any other non-coding actions\n"

            "Important: When you encounter a file that already exists but is empty, do not propose to create a new one. Instead, treat it as an existing file and suggest modifications or updates to it.\n"
            "FOR EACH FILE THAT NEEDS TO BE WORKED ON, WHETHER NEW, EXISTING, OR IMAGE, BE CLEAR AND SPECIFIC. MENTION ALL DETAILS, DO NOT PROVIDE ASSUMPTIONS, GUESSES, OR PLACEHOLDERS.\n"
            "No Yapping: Provide concise, focused responses without unnecessary elaboration or repetition. Stick strictly to the requested information and guidelines.\n\n"
            "Only return sections that are needed for the user request. Do not return non-relevant sections. STRICTLY ENFORCE IMAGE FORMAT RULES:\n\n"
            "- ONLY consider PNG, png, JPG, jpg, JPEG, jpeg, or .ico formats as eligible images\n"
            "- IMMEDIATELY REJECT any other image formats including SVG\n"
            "- SVG or other formats DO NOT COUNT as images needing generation\n"
            "- Only flag image generation if the plan EXPLICITLY includes generating new images in the eligible formats\n\n"
            "Special ending rules:\n"
            "- If plan includes BOTH dependencies AND new images in eligible formats: End with #### DONE: *** - D*** I**\n" 
            "- If ONLY dependencies need installing: End with #### DONE: *** - D***\n"
            "- If ONLY new eligible format images need generating: End with #### DONE: *** - I**\n"
            "- If NO dependencies AND NO eligible format images: No special ending"
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
        self.conversation_history.append({"role": "user", "content":  f"Here are the current project structure and files summary:\n{all_file_contents}\n"})
        self.conversation_history.append({"role": "assistant", "content": "Got it! Give me user prompt so i can support them."})

        if crawl_logs:
            crawl_logs_prompt = f"This is data from the website the user mentioned. You don't need to crawl again: {crawl_logs}"
            self.conversation_history.append({"role": "user", "content": crawl_logs_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Understood. Using provided data only."})

            utilization_prompt = (
                "Specify which file(s) should access this crawl data. "
                "Do not provide steps for crawling or API calls. "
                "The data is already available. "
                "Follow the original development plan guidelines strictly, "
                "ensuring adherence to all specified requirements and best practices."
            )
            self.conversation_history.append({"role": "user", "content": utilization_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Will specify files for data access, following original implementation guidelines strictly. No additional crawling or API calls needed."})

        if context:
            working_files = [file for file in context.get('working_files', []) if not file.lower().endswith(('.mp4', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.wav', '.mp3', '.ogg'))]

            all_working_files_contents = ""

            if working_files:
                for file_path in working_files:
                    file_content = read_file_content(file_path)
                    if file_content:
                        all_working_files_contents += f"\n\nFile: {file_path}: {file_content}"
                    else:
                        all_working_files_contents += f"\n\nFile: {file_path}: EXISTING EMPTY FILE -  NO NEW CREATION NEED PLEAS, ONLY MODIFIED IF NEED"


            if all_working_files_contents:
                self.conversation_history.append({"role": "user", "content": f"This is data for potential existing files you may need to modify or update or provided context. Even if a file's content is empty. \n{all_working_files_contents}"})
                self.conversation_history.append({"role": "assistant", "content": "Understood."})
            else:
                self.conversation_history.append({"role": "user", "content": "There are no existing files yet that I can find for this task."})
                self.conversation_history.append({"role": "assistant", "content": "Understood."})


        all_attachment_file_contents = ""

        # Process image files
        image_files = process_image_files(file_attachments)
        
        # Remove image files from file_attachments
        file_attachments = [f for f in file_attachments if not f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png'))]

        if file_attachments:
            for file_path in file_attachments:
                file_content = read_file_content(file_path)
                if file_content:
                    all_attachment_file_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if all_attachment_file_contents:
            self.conversation_history.append({"role": "user", "content": f"User has attached these files for you, use them appropriately: {all_attachment_file_contents}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood."})

        message_content = [{"type": "text", "text": "User has attached these images. Use them correctly, follow the user prompt, and use these images as support!"}]

        # Add image files to the user content
        for base64_image in image_files:
            message_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"{base64_image}"
                }
            })

        if assets_link:
            for image_url in assets_link:
                message_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                })

        self.conversation_history.append({"role": "user", "content": message_content})
        self.conversation_history.append({"role": "assistant", "content": "Understood."})

        if assets_link or image_files:
            image_detail_prompt = (
                "You MUST provide an extremely detailed analysis of each image according to the user's requirements.\n\n"
                "For EACH image, describe in precise detail:\n"
                "1. Visual Elements:\n"
                "   - Exact shapes and geometric forms used\n" 
                "   - Complete color palette with specific hex codes\n"
                "   - Precise alignments (center, left, right, justified)\n"
                "   - Layout arrangements and positioning\n"
                "   - Spacing and padding measurements\n\n"
                "2. Content Analysis:\n"
                "   - All text content with exact fonts and sizes\n"
                "   - Every icon and graphic element\n"
                "   - Patterns and textures\n"
                "   - Interactive elements\n\n"
                "3. Design Implementation:\n"
                "   - Exact pixel dimensions\n"
                "   - Specific margins and padding\n"
                "   - Component hierarchy and structure\n"
                "   - Responsive behavior if applicable\n\n"
                "4. Context & Purpose:\n"
                "   - Whether this needs to be an exact replica or just inspiration\n"
                "   - How it aligns with user requirements\n"
                "   - Any modifications needed from original\n\n"
                "Your description must be thorough enough that another agent can implement it perfectly without seeing the original image."
            )
            self.conversation_history.append({"role": "user", "content": image_detail_prompt})
            self.conversation_history.append({"role": "assistant", "content": "I will analyze each image with extreme detail, providing comprehensive specifications for all visual elements, content, measurements, and implementation requirements. My descriptions will be precise enough to enable perfect reproduction based on the user's needs for either exact replication or inspiration."})

    async def get_idea_plan(self, user_prompt, original_prompt_language):
        logger.debug("Generating idea plan based on user prompt")
        prompt = (
            f"Create a detailed implementation plan for:\n\n{user_prompt}\n\n"
            f"Operating System: {platform.system()}\n"
            f"All file paths and directory structures must use correct OS-specific separators and formatting.\n\n"
            f"CORE PRINCIPLES:\n"
            f"1. For landing pages and simple multi-page websites:\n"
            f"   - Use pure HTML/CSS by default\n" 
            f"   - Avoid React, TypeScript, or complex frameworks unless:\n"
            f"     * Explicitly requested by user\n"
            f"     * Advanced functionality requirements exist\n\n"
            f"#### Project Overview\n"
            f"Clearly define:\n"
            f"- Ultimate goal and main objectives\n"
            f"- Desired final outcome\n"
            f"- Success criteria\n\n"
            "#### Design System\n"
            "1. Visual Language:\n"
            "   - Overall aesthetic direction and mood\n"
            "   - Precise color palette with hex codes\n"
            "   - Typography system:\n"
            "     * Approved font families:\n"
            "       - System fonts: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial\n"
            "       - Web fonts: Roboto, Open Sans, Lato, Montserrat (Google Fonts only)\n"
            "       - NO custom font files (.woff/.woff2)\n"
            "     * Font scale (rem-based):\n"
            "       Desktop:\n"
            "       - h1: 2rem (32px)\n"
            "       - h2: 1.75rem (28px)\n"
            "       - h3: 1.5rem (24px)\n"
            "       - h4: 1.25rem (20px)\n"
            "       - Body: 1rem (16px)\n"
            "       - Small: 0.875rem (14px)\n"
            "       - Micro: 0.75rem (12px)\n\n"
            "       Mobile:\n"
            "       - h1: 1.75rem (28px)\n"
            "       - h2: 1.5rem (24px)\n"
            "       - h3: 1.25rem (20px)\n"
            "       - h4: 1.125rem (18px)\n"
            "       - Body: 1rem (16px)\n"
            "       - Small: 0.875rem (14px)\n"
            "       - Micro: 0.75rem (12px)\n"
            "     * Typography details:\n"
            "       - Font weights: 400 regular, 700 bold\n"
            "       - Line heights:\n"
            "         > Headings: 1.2-1.3\n"
            "         > Body: 1.5-1.6\n"
            "         > Small: 1.4\n"
            "       - Letter spacing:\n"
            "         > Headings: -0.02em\n"
            "         > Body: normal\n"
            "   - Language specifications:\n"
            "     * Primary language(s)\n"
            "     * Secondary language(s)\n"
            "     * Text direction (LTR/RTL)\n"
            "     * Character set requirements\n"
            "   - Layout principles and spacing system\n\n"
            "2. Core Features:\n"
            "   - Essential v1 components\n"
            "   - Key user interactions\n"
            "   - Must-have functionality\n"
            "   - Navigation architecture\n"
            "   - Language switching (if multilingual)\n\n"
            "3. Interactive Elements:\n"
            "   - Animation specifications\n"
            "   - Interactive components\n"
            "   - Responsive design rules\n"
            "   - Accessibility requirements\n"
            "   - Language-specific text rendering\n\n"
            "4. Brand Guidelines:\n"
            "   - Logo usage rules\n"
            "   - Brand color application\n"
            "   - Tone of voice per language\n"
            "   - Typography hierarchy\n"
            "   - Visual consistency standards\n"
            "   - Cultural considerations\n\n"
            "#### File Implementation Requirements\n"
            "For EACH file in scope:\n\n"
            "1. Existing Files:\n"
            "   - Current structure and content\n"
            "   - Functionality overview\n"
            "   - Dependencies\n"
            "   - Known limitations\n\n"
            "2. Reference Files:\n"
            "   - Source files to learn from\n"
            "   - Patterns to replicate\n"
            "   - Implementation details\n"
            "   - Adaptation guidelines\n\n"
            "3. Modifications:\n"
            "   - Detailed changes needed\n"
            "   - New features to add\n"
            "   - Elements to remove\n"
            "   - Dependency updates\n\n"
            "4. Technical Details:\n"
            "   - Component architecture\n"
            "   - Data flow patterns\n"
            "   - API integration specs\n"
            "   - Error handling strategy\n\n"
            "5. Integration:\n"
            "   - Component connections\n"
            "   - Required props\n"
            "   - Event handlers\n"
            "   - Data passing methods\n\n"
            "6. Asset Management:\n"
            "   Image Requirements:\n"
            "   - File location and name\n"
            "   - Purpose and placement\n"
            "   - Dimensions and format\n"
            "   - Source/generation method\n"
            "   - Usage context\n"
            "   - Required modifications\n\n"
            "   Format Guidelines:\n"
            "   SVG (MANDATORY for ALL icons and vector graphics - NO EXCEPTIONS):\n"
            "   - ALL UI/Navigation icons\n"
            "   - ALL logos and brand assets\n"
            "   - ALL social media icons\n"
            "   - ALL decorative illustrations\n"
            "   - ALL interface elements\n"
            "   - ALL interactive icons\n"
            "   - ALL small-scale graphics\n\n"
            "   PNG:\n"
            "   - Complex icons with transparency (only if SVG not possible)\n"
            "   - Text-heavy screenshots\n"
            "   - Badges requiring transparency\n\n"
            "   JPG:\n"
            "   - High-quality product photos\n"
            "   - Large background images\n"
            "   - Photo-realistic banner graphics\n"
            "   - Complex marketing visuals\n\n"
            "   Size Standards:\n"
            "   Icons (SVG preferred):\n"
            "   - Small: 24x24px\n"
            "   - Medium: 128x128px\n"
            "   - Large: 512x512px\n\n"
            "   Illustrations (SVG for simple, PNG/JPG for complex):\n"
            "   - Small: 400x400px\n"
            "   - Medium: 800x600px\n"
            "   - Large: 1024x1024px\n\n"
            "   Product Images (JPG/PNG only):\n"
            "   - Thumbnail: 400x400px\n"
            "   - Detail: 1200x1200px\n"
            "   - Full: 2048x2048px\n\n"
            "#### Interactive Component Requirements\n"
            "1. Maps:\n"
            "   - Use live map services (Google Maps, Mapbox, etc)\n"
            "   - Implement interactive controls\n"
            "   - Handle map events\n"
            "   - NO static images\n\n"
            "2. Calendars:\n"
            "   - Use calendar libraries\n"
            "   - Handle dates/times properly\n"
            "   - Support events and time zones\n"
            "   - NO static schedules\n\n"
            "3. Dynamic Components:\n"
            "   - Use proper libraries\n"
            "   - Implement state management\n"
            "   - Include error handling\n"
            "   - Support real-time updates\n\n"
            "#### File Organization\n"
            "Naming Rules:\n"
            "1. Check for existing similar names\n"
            "2. Use descriptive, unique names\n"
            "3. Follow project conventions\n"
            "4. Avoid generic names\n"
            "5. Include version numbers if needed\n"
            "6. Use correct extensions\n"
            "7. Add clear prefixes/suffixes\n"
            "8. Verify no naming conflicts\n"
            "9. Include dimensions for images\n"
            "10. Use lowercase for assets\n\n"
            "#### Styling Architecture\n"
            "Every UI component MUST have dedicated styles:\n\n"
            "HTML/CSS Projects:\n"
            "project_root/\n"
            "├── styles/\n"
            "│   └── main.css\n"
            "├── css/\n"
            "│   ├── index.css\n"
            "│   └── [page].css\n"
            "└── [page].html\n\n"
            "Rules:\n"
            "- One CSS per HTML file\n"
            "- Required index.css\n"
            "- No style sharing\n"
            "- No inline styles\n"
            "- Match filenames\n\n"
            "Framework Projects:\n"
            "React/Next.js:\n"
            "src/\n"
            "├── styles/\n"
            "│   └── [global styles]\n"
            "└── components/\n"
            "    └── [Component]/\n"
            "        ├── Component.tsx\n"
            "        └── Component.module.css\n\n"
            "Vue.js:\n"
            "src/\n"
            "└── components/\n"
            "    └── [Component].vue (with scoped styles)\n\n"
            "Angular:\n"
            "src/\n"
            "└── app/\n"
            "    └── components/\n"
            "        └── [component]/\n"
            "            ├── component.ts\n"
            "            └── component.scss\n\n"
            "Svelte:\n"
            "src/\n"
            "└── components/\n"
            "    └── Component.svelte (with styles)\n\n"
            "#### Directory Structure\n"
            "ONLY show:\n"
            "1. New files\n"
            "2. Moved files\n"
            "3. New/moved images\n"
            "Use single tree structure\n"
            "Verify unique paths\n\n"
            f"#### Build Commands\n"
            f"If required, provide {platform.system()}-specific commands for installing dependencies for this task:\n"
            f"```bash\n"
            f"# Node.js/npm dependencies\n"
            f"npm install [package-name]@[version] --save  # For production dependencies\n"
            f"npm install [package-name]@[version] --save-dev  # For development dependencies\n\n"
            f"# Python dependencies\n"
            f"pip install [package-name]==[version]  # For specific version\n"
            f"pip install [package-name]  # For latest version\n\n"
            f"# Ruby dependencies\n"
            f"gem install [package-name] -v [version]  # For specific version\n"
            f"gem install [package-name]  # For latest version\n\n"
            f"# PHP/Composer dependencies\n"
            f"composer require [vendor/package]:[version]  # For specific version\n"
            f"composer require [vendor/package]  # For latest version\n"
            f"```\n\n"
            f"IMPORTANT: Planning phase only - NO implementation code\n"
            f"Response language: {original_prompt_language}\n"
            f"Use markdown links: [text](url)\n\n"
            "Only return sections that are needed anc actionable for the user request. Do not return non-relevant sections."
            "IMPORTANT: This is a planning phase only - focus on clear, actionable steps and requirements. No implementation code should be provided."
            "Only return sections that are needed for the user request. Do not return non-relevant sections. If the plan includes dependencies that need to be installed and images that need to be newly generated in these formats only: 'PNG, png, JPG, jpg, JPEG, jpeg, and ico', then at the end of everything, the last sentence must start with #### DONE: *** - D*** I**. If only dependencies need to be installed, end with #### DONE: *** - D***. If only images need to be generated in the eligible formats, end with #### DONE: *** - I**. If neither dependencies nor images are needed, do not include any special ending.\n\n"
        )
        

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            response = await self.ai.arch_stream_prompt(self.conversation_history, 4096, 0.2, 0.1)
            return response
        except Exception as e:
            logger.error(f"`IdeaDevelopment` agent encountered an error: {e}")
            return {
                "reason": str(e)
            }

    async def get_idea_plans(self, user_prompt, original_prompt_language):
        logger.debug("Initiating idea plan generation process")
        return await self.get_idea_plan(user_prompt, original_prompt_language)
