const { driver } = require('@rocket.chat/sdk');
const respmap = require('./reply');

// Environment setup (consider using environment variables)
const HOST = 'localhost:3000';
const USER = 'rocket.cat';
const PASS = 'jobbench';
const BOTNAME = 'rocket cat';
const SSL = false;
const ROOMS = ['general'];
var myUserId;

// Bot configuration
const runbot = async () => {
    try {
        const conn = await driver.connect({ host: HOST, useSsl: SSL, timeout: 5000 });
        myUserId = await driver.login({ username: USER, password: PASS });
        const roomsJoined = await driver.joinRooms(ROOMS);
        console.log('joined rooms');

        const subscribed = await driver.subscribeToMessages();
        console.log('subscribed');

        const msgloop = await driver.reactToMessages(processMessages);
        console.log('connected and waiting for messages');

        const sent = await driver.sendToRoom(BOTNAME + ' is listening ...', ROOMS[0]);
        console.log('Greeting message sent');
    } catch (error) {
        console.error("Error:", error);
    }
};

// Process messages
const processMessages = async (err, message, messageOptions) => {
    if (!err) {
        if (message.u._id === myUserId) return;
        const roomname = await driver.getRoomName(message.rid);
        console.log('got message ' + message.msg);


        var response;
        if (message.msg in respmap) {
            response = respmap[message.msg];
        } else {
            response = message.u.username + ', how can I' + ' help you with "' + message.msg + '"';
        }
        try {
            const sentmsg = await driver.sendToRoomId(response, message.rid);
        } catch (error) {
            console.error("Error sending message:", error);
        }
    }
};

runbot()