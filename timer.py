import argparse
import time
import sys
import os


def parse_args():
    parser = argparse.ArgumentParser(description="Countdown Timer")
    parser.add_argument("duration", type=int, help="Duration of the timer in seconds")
    return parser.parse_args()


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    print("Time's up!")


def play_alarm():
    if sys.platform == "win32":
        import winsound
        winsound.Beep(440, 1000)  # Frequency 440Hz, Duration 1 second
    else:
        os.system('say "Timer completed"')


def main():
    args = parse_args()
    countdown(args.duration)
    play_alarm()


if __name__ == "__main__":
    main()
