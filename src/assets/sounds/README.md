# Sound Files Directory

This directory contains audio files for notifications and alerts.

## Required Sound Files

To add custom sounds, place WAV or MP3 files here with these names:

- `break_reminder.wav` - Played when break is due
- `notification.wav` - General notification sound
- `warning.wav` - Warning alert sound
- `alert.wav` - Attention alert sound
- `achievement.wav` - Success/achievement sound

## Default Behavior

If sound files are not present, the application will:

1. Use system beep as fallback (Windows)
2. Play silently if system beep unavailable

## Sound Requirements

- **Format**: WAV or MP3
- **Sample Rate**: 44100 Hz recommended
- **Channels**: Mono or Stereo
- **Duration**: 0.5 - 3 seconds recommended
- **Volume**: Normalized to prevent clipping

## Free Sound Resources

- [Freesound](https://freesound.org/)
- [Zapsplat](https://www.zapsplat.com/)
- [SoundBible](http://soundbible.com/)

## Creating Custom Sounds

You can use tools like:

- [Audacity](https://www.audacityteam.org/) (Free)
- [Ocenaudio](https://www.ocenaudio.com/) (Free)
- Any audio editor

## Example

Place your sound file:

```
src/assets/sounds/break_reminder.wav
```

The application will automatically use it.
