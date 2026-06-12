#pragma once

#include <string>

namespace Corona::Events {

// Keyboard event: key down/up
struct KeyEvent {
	bool down = false;              // true=keyDown, false=keyUp
	std::string code;               // physical key code or code string
	std::string modifiers;          // comma-separated modifiers
	std::string display_key;        // printable/display key
};

// Mouse button event: click/mousedown/mouseup
struct MouseButtonEvent {
	std::string event_type;         // e.g. "click", "mousedown", "mouseup"
	std::string button;             // button id/name
	double x = 0.0;                 // x coordinate
	double y = 0.0;                 // y coordinate
};

// Mouse move event (continuous)
struct MouseMovedEvent {
	double x = 0.0;
	double y = 0.0;
};

} // namespace Corona::Events
