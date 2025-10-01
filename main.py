from Head.Ear import takeCommand
from Brain.processor import process
from Head.Mouth import say
import sys

if __name__ == "__main__":
    say("Your personal assistant is ready, at your service, sir")
    print("🤖 BuddyBug is ready...")

    while True:
        query = takeCommand(duration=7)  # duration in seconds
        if query:
            query_lower = query.lower().strip()  # normalize input for comparison

            # Quit condition
            if query_lower in ["quit", "exit", "stop","fuck off", "Ok, fuck off"]:
                say("Goodbye boss, see you agin.")
                sys.exit()

            # Otherwise process normally
            response = process(query)
            print("BuddyBug:", response)
            say(response)
