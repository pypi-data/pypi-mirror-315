import subprocess
import os
import asyncio
import logging
import json
import requests


logger = logging.getLogger("uvicorn")

class RuneLiteClient:
    def __init__(self, display=":1", jar_path="/usr/local/bin/runelite.jar"):
        self.display = display
        self.jar_path = jar_path

    async def start_runelite_async(self):
        env = os.environ.copy()
        env["DISPLAY"] = self.display

        # Schedule the subprocess to run in the background without waiting for it
        asyncio.create_task(self._run_subprocess_in_background(env))

        # Return immediately
        return "RuneLite is starting in the background."


    async def _run_subprocess_in_background(self, env):
        try:
            max_memory = "512m"
            initial_memory = "256m"
            # Run the subprocess in a thread pool without blocking the main coroutine
            await asyncio.to_thread(
            subprocess.run,
            [
                "java",
                f"-Xmx{max_memory}",
                f"-Xms{initial_memory}", 
                "-jar",
                self.jar_path
            ],
            env=env
        )
            logger.info("RuneLite started successfully.")
        except Exception as e:
            logger.error(f"Failed to start RuneLite: {e}")

    async def stop_runelite_async(self):
        try:
            # Use pkill to terminate the process by its name or part of the name
            #await asyncio.to_thread(subprocess.run, ["pkill", "-f", "runelite.jar"])
            await asyncio.to_thread(subprocess.run, ["pkill", "java"])
            logger.info("RuneLite stopped successfully.")
            return "RuneLite stopped successfully."
        except Exception as e:
            logger.error(f"Failed to stop RuneLite: {e}")
            return f"Failed to stop RuneLite: {e}"

    async def start_and_configure_runelite(self):
        # Start RuneLite client
        start_message = await self.start_runelite_async()
        logger.info(start_message)

        # Wait for a reasonable amount of time for RuneLite to create profiles.json
        await asyncio.sleep(60)  # Adjust the sleep time as necessary

        # Define the URLs and file paths
        url = 'https://kbve.com/data/outpost/runelite/default.properties'
        profiles_json_path = os.path.expanduser('~/.runelite/profiles2/profiles.json')
        destination_dir = os.path.expanduser('~/.runelite/profiles2/')

        # Read the profiles.json file
        try:
            with open(profiles_json_path, 'r') as f:
                profiles_data = json.load(f)
                # Assuming we want to use the ID from the first profile entry
                profile_id = profiles_data['profiles'][1]['id']  # Assuming "default" profile is the second entry
        except FileNotFoundError:
            logger.error(f"profiles.json not found at {profiles_json_path}")
            await self.stop_runelite_async()
            return "Failed: profiles.json not found"
        except (json.JSONDecodeError, IndexError, KeyError):
            logger.error(f"Error reading or parsing profiles.json")
            await self.stop_runelite_async()
            return "Failed: Error reading or parsing profiles.json"

        # Create the new file name
        new_file_name = f"default-{profile_id}.properties"
        new_file_path = os.path.join(destination_dir, new_file_name)

        # Download the default.properties file
        response = requests.get(url)
        if response.status_code == 200:
            default_properties = response.text
        else:
            logger.error(f"Failed to download default.properties. Status code: {response.status_code}")
            await self.stop_runelite_async()
            return f"Failed to download default.properties. Status code: {response.status_code}"

        # Write the downloaded content to the new file
        try:
            with open(new_file_path, 'w') as f:
                f.write(default_properties)
            logger.info(f"Successfully created {new_file_name} in {destination_dir}")
        except IOError as e:
            logger.error(f"Failed to write the file: {e}")
            await self.stop_runelite_async()
            return f"Failed to write the file: {e}"

        # Stop RuneLite client
        stop_message = await self.stop_runelite_async()
        logger.info(stop_message)

        return "RuneLite configured and stopped successfully."
        
    async def close(self):
        # This method is required by the KRDecorator's pattern, even if it does nothing
        pass

    async def status_runelite(self):
        """
        Check if the RuneLite (runelite.jar) process is running using `pgrep`.
        Returns a status message based on whether the process is found.
        """
        try:
            # Use `pgrep` to find the process by its name
            result = subprocess.run(
                ["pgrep", "-f", "runelite.jar"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Check if any process ID was found
            if result.stdout.strip():
                logger.info("RuneLite is currently running.")
                return "RuneLite is running."
            else:
                logger.info("RuneLite is not running.")
                return "RuneLite is not running."

        except Exception as e:
            logger.error(f"Error checking RuneLite status: {e}")
            return f"Error checking RuneLite status: {e}"