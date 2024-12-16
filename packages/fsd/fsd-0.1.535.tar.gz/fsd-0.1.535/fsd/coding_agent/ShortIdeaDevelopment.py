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

class ShortIdeaDevelopment:
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
            f"As a senior {role}, provide a concise, specific plan:\n\n"
            "File Updates\n"
            f"- {self.repo.get_repo_path()}/path/to/file1.ext:\n"
            "  - Update: [1-2 sentences what need to be done here!]\n"
            "  - Reason: [brief justification]\n"
            f"- {{self.repo.get_repo_path()}}/path/to/file2.ext:\n"
            "  - Update: [1-2 sentences what need to be done here!]\n"
            "  - Reason: [brief justification]\n\n"
            "New Files (only if file doesn't exist)\n"
            f"- {self.repo.get_repo_path()}/path/to/new_file1.ext:\n"
            "  - Implementation: [detailed description of what to implement]\n"
            f"- {self.repo.get_repo_path()}/path/to/new_file2.ext:\n"
            "  - Implementation: [detailed description of what to implement]\n\n"
            "Directory Structure (MANDATORY - ONLY for new files being added or files being moved):\n"
            "```plaintext\n"
            "project_root/\n"
            "├── path/                         # Only show directories containing new/moved files\n"
            "│   └── to/\n"
            "│       ├── new_file1.ext         # New file\n"
            "│       └── new_file2.ext         # New file\n"
            "└── new_location/                 # Only if files are being moved\n"
            "    └── moved_file.ext            # Moved from: old/path/moved_file.ext\n"
            "```\n"
            "IMPORTANT: Tree structure is MANDATORY but ONLY for:\n"
            "- New files being created\n" 
            "- Files being moved (must show source and destination)\n"
            "DO NOT include existing files that are only being modified in the tree.\n"
            "DO NOT include any files/directories not directly involved in additions/moves.\n\n"
            "Note: If no new files need to be created, omit the 'New Files' section.\n"
            "API Usage\n"
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
            "Asset Integration\n"
            "- Describe usage of image/video/audio assets in new files (filename, format, placement)\n"
            "- For new images: Provide content, style, colors, dimensions, purpose\n"
            "- For social icons: Specify platform (e.g., Facebook, TikTok), details, dimensions, format\n"
            "- Only propose creatable files (images, code, documents). No fonts or audio or video files.\n"

            "Dependencies Required (Only if task requires dependencies):\n"
            "For each file that requires dependencies, specify:\n"
            f"- {self.repo.get_repo_path()}/file_path:\n"
            "  - Existing Dependencies (if found in requirements.txt, package.json, etc):\n"
            "    - dependency_name: Explain specific usage in this file\n"
            "  - New Dependencies (if not found in any dependency files):\n"
            "    - dependency_name: Explain why needed and specific usage\n"
            "    - Version (only if specific version required)\n"
            "Note: Skip this section if task has no dependency requirements\n"

            "DO NOT MENTION THESE ACTIONS - (SINCE THEY WILL BE HANDLED AUTOMATICALLY): \n"
            "- Navigating to any location\n"
            "- Opening browsers or devices\n"
            "- Opening files\n"
            "- Any form of navigation\n"
            "- Verifying changes\n"
            "- Any form of verification\n"
            "- Clicking, viewing, or any other non-coding actions\n"

            "Project Setup and Default Tech Stacks:\n"
            "1. For Landing Pages (STRICT DEFAULT):\n"
            "   - ALWAYS use Pure HTML/CSS/JavaScript for landing pages and multi-page websites\n" 
            "   - DO NOT use React, Vue, Angular or any framework unless explicitly requested\n"
            "   - Even for multiple pages, stick to pure HTML/CSS/JS by default\n"
            "   - Organized file structure:\n"
            "     * index.html (and other HTML pages)\n"
            "     * css/styles.css\n"
            "     * js/main.js\n"
            "   - CSS reset/normalize\n"
            "   - Mobile-first responsive design\n\n"

            "2. For Web Applications (Default):\n"
            "   - Vite + React + Shadcn UI (ONLY when specifically needed for complex applications)\n"
            "   - Never use Next.js unless explicitly requested\n"
            "   - Follow Vite project structure\n\n"

            "CSS Usage Guidelines by Tech Stack:\n"
            "1. Pure HTML/CSS Projects:\n"
            "   - Single styles.css file for small projects\n"
            "   - For larger projects:\n"
            "     * base.css (resets, typography)\n"
            "     * components.css (reusable components)\n"
            "     * layout.css (grid, structure)\n"
            "     * utilities.css (helper classes)\n\n"

            "2. React Projects:\n"
            "   - CSS Modules or Styled Components\n"
            "   - Component-scoped styles\n"
            "   - No global CSS except for base styles\n"
            "   - Follow framework conventions\n\n"

            "3. Vue Projects:\n"
            "   - Scoped component styles\n"
            "   - Single-file component pattern\n"
            "   - Style block with scoped attribute\n\n"

            "4. Angular Projects:\n"
            "   - Component-specific stylesheet\n"
            "   - ViewEncapsulation\n"
            "   - Follow Angular style guide\n\n"

            "CSS Best Practices (All Stacks):\n"
            "- Use appropriate methodology (BEM/SMACSS)\n"
            "- Avoid deep nesting\n"
            "- Minimize specificity conflicts\n"
            "- Follow stack-specific conventions\n"
            "- No CSS overengineering\n"

            "Always use the appropriate boilerplate command to initialize the project structure for new projects. Here's a detailed example for setting up a new Vite React project with Shadcn UI:\n\n"

            "1. Initialize a new Vite React project:\n"
            "   npm create vite@latest my-vite-react-app --template react\n"
            "   cd my-vite-react-app\n"
            "   npm install\n\n"

            "2. Install and set up Tailwind CSS (required for Shadcn UI):\n"
            "   npm install -D tailwindcss postcss autoprefixer\n"
            "   npx tailwindcss init -p\n\n"

            "3. Install Shadcn UI CLI:\n"
            "   npm i -D @shadcn/ui\n\n"

            "4. Initialize Shadcn UI:\n"
            "   npx shadcn-ui init\n\n"

            "5. Start adding Shadcn UI components as needed:\n"
            "   npx shadcn-ui add button\n"
            "   npx shadcn-ui add card\n"
            "   # Add more components as required\n\n"

            "After setup, the project structure should look like this:\n"
            "my-vite-react-app/\n"
            "├── public/\n"
            "├── src/\n"
            "│   ├── components/\n"
            "│   │   └── ui/\n"
            "│   │       ├── button.tsx\n"
            "│   │       └── card.tsx\n"
            "│   ├── App.tsx\n"
            "│   ├── index.css\n"
            "│   └── main.tsx\n"
            "├── .gitignore\n"
            "├── index.html\n"
            "├── package.json\n"
            "├── postcss.config.js\n"
            "├── tailwind.config.js\n"
            "├── tsconfig.json\n"
            "└── vite.config.ts\n\n"

            "Ensure that the project structure adheres to these standards for easy deployment and maintenance.\n"

            "Important: When you encounter a file that already exists but is empty, do not propose to create a new one. Instead, treat it as an existing file and suggest modifications or updates to it.\n"
            "No Yapping: Provide concise, focused responses without unnecessary elaboration or repetition\n"
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
            self.conversation_history.append({"role": "assistant", "content": "Will specify files for data access, following original development plan guidelines strictly. No additional crawling or API calls needed."})
        
        if context:
            working_files = [file for file in context.get('working_files', []) if not file.lower().endswith(('.mp4', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.wav', '.mp3', '.ogg'))]

            all_working_files_contents = ""
          

            if working_files:
                for file_path in working_files:
                    file_content = read_file_content(file_path)
                    if file_content:
                        all_working_files_contents += f"\n\nFile: {file_path}: {file_content}"
                    else:
                        all_working_files_contents += f"\n\nFile: {file_path}: EXISTING EMPTY FILE - NO NEW CREATION NEED PLEAS, ONLY MODIFIED IF NEED"

            if all_working_files_contents:
                self.conversation_history.append({"role": "user", "content": f"This is data for potential existing files you may need to modify or update or provide context. \n{all_working_files_contents}"})
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
                "   - Precise alignments (left/right/center/justified)\n"
                "   - Layout arrangements and positioning\n"
                "   - Spacing and padding measurements\n\n"
                "2. Content Analysis:\n"
                "   - All text content with exact fonts and sizes\n"
                "   - Every icon and graphic element\n"
                "   - Patterns and textures\n"
                "   - Image assets and their placement\n\n"
                "3. Implementation Requirements:\n"
                "   - Exact pixel dimensions\n"
                "   - Specific margins and padding\n"
                "   - Component hierarchy and structure\n"
                "   - Interactive elements and states\n\n"
                "4. Context & Purpose:\n"
                "   - Whether this needs to be an exact replica or just inspiration\n"
                "   - How closely to follow the reference image\n"
                "   - Which elements are essential vs optional\n"
                "   - Any modifications needed to match user requirements\n\n"
                "Your description must be thorough enough that another agent can implement it perfectly without seeing the original image."
            )
            self.conversation_history.append({"role": "user", "content": image_detail_prompt})
            self.conversation_history.append({"role": "assistant", "content": "I will analyze each image with extreme detail, covering all visual elements, content, measurements, and implementation requirements. I'll clearly indicate whether each image should be replicated exactly or used as inspiration, ensuring other agents can implement the design precisely as needed."})

    async def get_idea_plan(self, user_prompt, original_prompt_language):
        logger.debug("Generating idea plan based on user prompt")
        prompt = (
            f"Provide a clear, organized implementation plan for:\n\n{user_prompt}\n\n"
            "#### Ultimate Goal\n"
            "Clearly describe what this implementation will achieve for the user when completed.\n\n"
            "#### File Analysis\n"
            "For EACH file that needs to be worked on:\n\n"
            "1. File Type & Status\n"
            "   - New file to be created\n"
            "   - Existing file to modify\n"
            "   - Reference file to learn from\n"
            "   - Full path and location\n"
            "   - Parent directory structure\n\n"
            "2. File Content & Structure\n"
            "   - For existing files:\n"
            "     * Current components and features\n" 
            "     * Existing dependencies\n"
            "     * Integration points\n"
            "   - For new files:\n"
            "     * Required components\n"
            "     * Dependencies needed\n"
            "     * Integration requirements\n"
            "   - For reference files:\n"
            "     * Key patterns to adopt\n"
            "     * Implementation details\n"
            "     * Architecture decisions\n\n"
            "#### Design System\n"
            "1. Typography\n"
            "   - ONLY use system fonts or Google Fonts\n"
            "   - NO custom font files (.woff/.woff2/etc)\n"
            "   - Font sizes (in px/rem):\n"
            "     * Headings: h1 (24px/1.5rem), h2 (20px/1.25rem), h3 (18px/1.125rem)\n"
            "     * Body: 16px/1rem\n"
            "     * Small: 14px/0.875rem\n"
            "     * Micro: 13px/0.8125rem\n"
            "   - Font weights: 400 regular, 500 medium, 700 bold\n"
            "   - Line heights: 1.2 to 1.6\n"
            "   - Letter spacing: -0.5px to 0.5px\n\n"
            "2. Colors\n"
            "   - Primary palette with hex codes\n"
            "   - Secondary palette with hex codes\n"
            "   - Accent colors with hex codes\n"
            "   - State colors (hover, active, disabled)\n\n"
            "3. Spacing & Layout\n"
            "   - Grid system specifications\n"
            "   - Spacing scale (4px increments)\n"
            "   - Margins and padding (in px)\n"
            "   - Breakpoints for responsive design\n\n"
            "4. Components\n"
            "   - Core UI components with exact measurements:\n"
            "     * Buttons: height, width, padding\n"
            "     * Forms: input sizes, spacing\n"
            "     * Cards: dimensions, margins\n"
            "   - Interactive states\n"
            "   - Animation timings (200-500ms)\n\n"
            "#### Implementation Rules\n"
            "1. File Organization\n"
            "   - Each component MUST have dedicated CSS file\n"
            "   - Each page MUST have dedicated CSS file\n"
            "   - Every index.html MUST have matching index.css\n"
            "   - Global styles in global.css only\n"
            "   - Main application styles in main.css\n\n"
            "2. Functional Features\n"
            "   - Maps: Use actual map libraries (Google Maps, Leaflet)\n"
            "   - Calendars: Use proper scheduling components\n"
            "   - Charts: Use charting libraries\n"
            "   - NO static images for functional elements\n\n"
            "3. Image Assets\n"
            "   SVG Usage:\n"
            "   - Logos requiring scaling\n"
            "   - UI/Navigation icons\n"
            "   - Social media icons\n"
            "   - Simple illustrations\n\n"
            "   PNG Usage:\n"
            "   - Icons needing transparency\n"
            "   - UI elements with clarity needs\n"
            "   - Badges and symbols\n\n"
            "   JPG Usage:\n"
            "   - Product photography\n"
            "   - Background images\n"
            "   - Banner images\n\n"
            "   Size Guidelines:\n"
            "   - Icons: 24x24px (small), 128x128px (medium), 512x512px (large)\n"
            "   - Illustrations: 400x400px (small), 800x600px (medium), 1024x1024px (large)\n"
            "   - Product Images: 400x400px (thumbnails), 1200x1200px (detail), 2048x2048px (full)\n\n"
            "#### Required File Structure\n"
            "src/\n"
            "├── styles/\n"
            "│   ├── global.css     # Global styles only\n"
            "│   └── main.css       # Main application styles\n"
            "├── components/        # Each with dedicated CSS\n"
            "│   ├── ComponentName/\n"
            "│   │   ├── ComponentName.jsx\n"
            "│   │   └── ComponentName.css\n"
            "└── pages/            # Each with dedicated CSS\n"
            "    └── PageName/\n"
            "        ├── PageName.jsx\n"
            "        ├── PageName.css\n"
            "        ├── index.html\n"
            "        └── index.css  # Required for index.html\n\n"
            f"#### System Information\n"
            f"OS: {platform.system()}\n"
            f"Use appropriate path separators for the OS above.\n\n"
            f"#### Directory Structure\n"
            "Provide ONE unified tree showing ONLY:\n"
            "- New files being added\n"
            "- Files being moved\n"
            "- New/moved image assets\n"
            "- Required index.css for any index.html\n"
            "DO NOT include modified files or duplicate paths\n\n"
            f"Response Language: {original_prompt_language}\n\n"
            "CRITICAL REMINDERS:\n"
            "- This is a PLANNING phase - NO implementation code\n"
            "- Verify all paths are unique and clear\n"
            "- Ensure every index.html has index.css\n"
            "- Use only system fonts or Google Fonts\n"
            "- Implement functional features with actual components\n"
            "- Provide full paths for all affected files\n"
            "- Be specific about file status (new/existing/reference)\n"
            "- Include only absolutely necessary files and images\n"
            "- Use markdown format for links: [text](url)"
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
