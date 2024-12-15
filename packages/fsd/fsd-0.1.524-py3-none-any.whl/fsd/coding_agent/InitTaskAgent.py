import os
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class InitTaskAgent:
    """
    A class to analyze project structure and determine if a React + TypeScript + Vite template should be used.
    """

    def __init__(self, repo):
        """
        Initialize the InitTaskAgent with necessary configurations.

        Args:
            repo: Repository object containing project information
        """
        self.max_tokens = 4096
        self.repo = repo
        self.ai = AIGateway()

    async def analyze_project_structure(self, prompt):
        """
        Analyze project structure and user prompt to determine if React + TypeScript + Vite template should be used.

        Args:
            prompt (str): The user's instruction/prompt

        Returns:
            dict: Analysis result indicating if template should be used
        """
        logger.debug("\n #### The `InitTaskAgent` is analyzing project structure")
        messages = [
            {
                "role": "system", 
                "content": (
                    "You are an expert project structure analyzer. Your goal is to:\n\n"
                    "1. Analyze the project tree structure to determine if it's an empty/new project\n"
                    "2. Review the user's prompt to check if it enforces any specific tech stack\n"
                    "3. Check if the project already has an established structure (e.g. package.json, tsconfig.json, etc)\n"
                    "4. Check if the project already uses a different framework/stack\n"
                    "5. For landing pages:\n"
                    "   - If it's a simple landing page with basic content and minimal interactivity, use plain HTML/CSS\n"
                    "   - Only use React + TypeScript + Vite if the landing page requires complex functionality like:\n"
                    "     * Advanced state management\n"
                    "     * Complex user interactions\n"
                    "     * Dynamic data handling\n"
                    "     * Integration with backend services\n"
                    "     * Complex animations/transitions\n"
                    "6. Determine if using React + TypeScript + Vite template would be appropriate\n\n"
                    "Return result as:\n"
                    "- 0: Do not use template if any of these are true:\n"
                    "  - Project not empty\n"
                    "  - Prompt enforces different stack\n"
                    "  - Project has existing structure files\n"
                    "  - Project already uses different framework\n"
                    "  - Simple landing page that only needs HTML/CSS\n"
                    "- 1: Use React + TypeScript + Vite template only if:\n"
                    "  - Project is empty/new\n"
                    "  - User prompt involves complex web functionality\n"
                    "  - Landing page requires advanced features beyond basic HTML/CSS\n"
                    "  - User prompt aligns with React/TypeScript capabilities\n"
                    "  - No conflicting tech requirements\n"
                    "  - No existing project structure\n\n"
                    "Respond with JSON format:\n"
                    "{\n"
                    '    "result": 0/1\n'
                    "}"
                )
            },
            {
                "role": "user",
                "content": f"Project structure:\n{self.repo.print_tree()}\n\nUser prompt:\n{prompt}\n\nAnalyze if this is an empty/new project without existing structure and if the prompt requires React + TypeScript + Vite template or can be built with simple HTML/CSS."
            }
        ]

        try:
            logger.debug("\n #### The `InitTaskAgent` is sending request to AI Gateway")
            response = await self.ai.prompt(messages, 4096, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### The `InitTaskAgent` successfully parsed AI response")
            return res
        except json.JSONDecodeError:
            logger.debug("\n #### The `InitTaskAgent` encountered JSON decode error, attempting repair")
            good_json_string = repair_json(response.choices[0].message.content)
            result_json = json.loads(good_json_string)
            logger.debug("\n #### The `InitTaskAgent` successfully repaired and parsed JSON")
            return result_json
        except Exception as e:
            logger.error(f"The `InitTaskAgent` failed to analyze project: {e}")
            return {"result": 0}

    async def get_init_plan(self, prompt):
        """
        Get initialization plan based on project analysis.

        Args:
            prompt (str): The user's instruction/prompt

        Returns:
            dict: Analysis result indicating if template should be used
        """
        logger.debug("\n #### The `InitTaskAgent` is beginning project analysis")
        plan = await self.analyze_project_structure(prompt)
        logger.debug("\n #### The `InitTaskAgent` completed project analysis")
        return plan
