const index = require('../index');
const { getMessage, main } = index;

describe('getMessage', () => {
  test('returns correct string', () => {
    expect(getMessage()).toBe('CodePilot execution successful');
  });

  test('throws when called with arguments', () => {
    expect(() => getMessage('unexpected')).toThrow(TypeError);
  });

  test('throws with correct message when called with arguments', () => {
    expect(() => getMessage('arg')).toThrow('getMessage does not accept arguments');
  });

  test('returns a string type', () => {
    const result = getMessage();
    expect(typeof result).toBe('string');
  });
});

describe('main', () => {
  beforeEach(() => {
    jest.restoreAllMocks();
  });

  test('logs the success message', () => {
    const logSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
    main();
    expect(logSpy).toHaveBeenCalledWith('CodePilot execution successful');
    logSpy.mockRestore();
  });

  test('handles errors gracefully when getMessage throws', () => {
    const error = new Error('test error');
    jest.spyOn(index, 'getMessage').mockImplementation(() => { throw error; });
    const errorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    const exitSpy = jest.spyOn(process, 'exit').mockImplementation(() => {});
    main();
    expect(errorSpy).toHaveBeenCalledWith('Error:', error.message);
    expect(exitSpy).toHaveBeenCalledWith(1);
    errorSpy.mockRestore();
    exitSpy.mockRestore();
  });

  test('handles non-string message gracefully', () => {
    jest.spyOn(index, 'getMessage').mockImplementation(() => 123);
    const errorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    const exitSpy = jest.spyOn(process, 'exit').mockImplementation(() => {});
    main();
    expect(errorSpy).toHaveBeenCalledWith('Error:', 'Message must be a string');
    expect(exitSpy).toHaveBeenCalledWith(1);
    errorSpy.mockRestore();
    exitSpy.mockRestore();
  });

  test('does not exit process on success', () => {
    const exitSpy = jest.spyOn(process, 'exit').mockImplementation(() => {});
    const logSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
    main();
    expect(exitSpy).not.toHaveBeenCalled();
    logSpy.mockRestore();
    exitSpy.mockRestore();
  });
});