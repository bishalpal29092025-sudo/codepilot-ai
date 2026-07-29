'use strict';

/**
 * Returns the success message.
 * @returns {string}
 * @throws {TypeError} If called with arguments.
 */
function getMessage(...args) {
  try {
    if (args.length > 0) {
      throw new TypeError('getMessage does not accept arguments');
    }
    return "CodePilot execution successful";
  } catch (err) {
    // Preserve original error type and message for callers
    throw err;
  }
}

/**
 * Main entry point for CLI.
 * Executes getMessage and logs the result.
 * Handles any unexpected errors gracefully.
 * @returns {void}
 */
function main() {
  try {
    const message = getMessage();
    if (typeof message !== "string") {
      throw new TypeError("Message must be a string");
    }
    console.log(message);
  } catch (err) {
    console.error("Error:", err.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { getMessage, main };
