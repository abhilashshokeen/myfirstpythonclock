import datetime
import os
import sys
import time

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


def play_alarm_sound(sound_path: str = None):
    """Plays an alarm sound or falls back to system beeps."""
    if PYGAME_AVAILABLE and sound_path and os.path.exists(sound_path):
        pygame.mixer.init()
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)  # Loop indefinitely
        input("\nPress [Enter] to turn off the alarm: ")
        pygame.mixer.music.stop()
    else:
        # Fallback: cross-platform terminal beep if no audio file is provided
        print("\a" * 5)
        if sys.platform == "win32":
            import winsound
            for _ in range(5):
                winsound.Beep(1000, 800)
                time.sleep(0.2)
        else:
            for _ in range(5):
                sys.stdout.write("\a")
                sys.stdout.flush()
                time.sleep(0.5)
        input("\nPress [Enter] to dismiss: ")


def set_alarm():
    print("=== Python Terminal Alarm Clock ===")
    
    # Prompt and validate user input
    while True:
        target_input = input("Enter alarm time (HH:MM or HH:MM:SS in 24-hr format): ").strip()
        time_format = "%H:%M:%S" if target_input.count(":") == 2 else "%H:%M"
        
        try:
            parsed_time = datetime.datetime.strptime(target_input, time_format).time()
            break
        except ValueError:
            print("Invalid format. Please use HH:MM (e.g., 07:30) or HH:MM:SS (e.g., 07:30:00).")

    # Calculate target datetime
    now = datetime.datetime.now()
    alarm_dt = datetime.datetime.combine(now.date(), parsed_time)
    
    # If the time has already passed today, schedule it for tomorrow
    if alarm_dt <= now:
        alarm_dt += datetime.timedelta(days=1)
        print(f"Time already passed for today. Setting alarm for tomorrow at {parsed_time}.")
    else:
        print(f"Alarm set for today at {parsed_time}.")

    print("Running... Press Ctrl+C to cancel.\n")

    # Countdown loop
    try:
        while True:
            remaining_seconds = int((alarm_dt - datetime.datetime.now()).total_seconds())
            
            if remaining_seconds <= 0:
                print("\n" + "=" * 30)
                print("⏰ WAKE UP! ALARM RINGING! ⏰")
                print("=" * 30)
                # Pass your custom audio file path here (e.g., 'alarm.mp3')
                play_alarm_sound("alarm.mp3")
                break

            # Format remaining time
            hours, remainder = divmod(remaining_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            sys.stdout.write(f"\rTime remaining: {hours:02d}:{minutes:02d}:{seconds:02d}")
            sys.stdout.flush()
            
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nAlarm cancelled.")


if __name__ == "__main__":
    set_alarm()
