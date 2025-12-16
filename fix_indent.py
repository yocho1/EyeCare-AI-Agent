"""Fix indentation in main_window.py"""

with open('src/ui/main_window.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix lines 381-395 (0-indexed: 380-394)
fixed_lines = lines[:380]

fixed_content = """        
        # For break_due, call directly - it's time critical!
        if update_type == 'break_due':
            self.logger.info("BREAK DUE - Calling modal DIRECTLY")
            try:
                self._show_break_modal(data.get('data', {}))
                self.logger.info("Break modal call completed")
            except Exception as e:
                self.logger.error(f"Break modal failed: {e}", exc_info=True)
        else:
            # Schedule other UI updates on main thread
            try:
                self.root.after(0, self._process_agent_update, data)
                self.logger.info(f"Scheduled _process_agent_update for {update_type}")
            except Exception as e:
                self.logger.error(f"Failed to schedule update: {e}", exc_info=True)
"""

fixed_lines.append(fixed_content)
fixed_lines.extend(lines[396:])

with open('src/ui/main_window.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("Fixed indentation!")
