import { spawn } from 'child_process';
import { logger } from './logger.js';

export function launchAgent({ isWindows, backgroundMode, baseURL, threadId, env }) {
  const pythonBin = isWindows ? './aiagent/venv/Scripts/python' : './aiagent/venv/bin/python';
  const script = backgroundMode ? './aiagent/background_mode/aiagent/main.py' : './aiagent/main.py';
  const proc = spawn(pythonBin, [script], { env });
  proc.stdout.on('data', (d) => logger.info(`[Agent stdout]: ${d}`));
  proc.stderr.on('data', (d) => logger.error(`[Agent stderr]: ${d}`));
  proc.on('error', (e) => logger.error('Agent failed to start:', e));
  proc.on('exit', (code) => logger.info(`Agent exited with code ${code}`));
  return proc;
}