// instances.js
import { SSocket } from './s_socket';
import { SActions } from './s_actions';

export const sSocket = new SSocket();
sSocket.setConnectionConfiguration('88.99.214.187', 12055);

export const sActions = new SActions(sSocket);
