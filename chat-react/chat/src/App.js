// chat/src/App.js

    import React, { Component } from 'react';
        // [..]
    import {
      handleInput,
      connectToChatkit,
    } from './methods';
    import Dialog from './components/Dialog';

    import 'skeleton-css/css/normalize.css';
    import 'skeleton-css/css/skeleton.css';
    import './App.css';

    class App extends Component {
      constructor() {
        super();
        this.state = {
          userId: '',
          showLogin: true,
          isLoading: false,
          currentUser: null,
          currentRoom: null,
          rooms: [],
          roomUsers: [],
          roomName: null,
          messages: [],
          newMessage: '',
        };

        this.handleInput = handleInput.bind(this);
        this.connectToChatkit = connectToChatkit.bind(this);
      }

      render() {
        const {// eslint-disable-next-line
          userId,// eslint-disable-next-line
          showLogin,// eslint-disable-next-line
          rooms,// eslint-disable-next-line
          currentRoom,// eslint-disable-next-line
          currentUser,// eslint-disable-next-line
          messages,// eslint-disable-next-line
          newMessage,// eslint-disable-next-line
          roomUsers,// eslint-disable-next-line
          roomName,// eslint-disable-next-line
        } = this.state;

        return (
          <div className="App">
            <aside className="sidebar left-sidebar">
              {currentUser ? (
              <div className="user-profile">
                <span className="username">{currentUser.name}</span>
                <span className="user-id">{`@${currentUser.id}`}</span>
              </div>
              ) : null}
            </aside>
            <section className="chat-screen">
              <header className="chat-header"></header>
              <ul className="chat-messages"></ul>
              <footer className="chat-footer">
                <form className="message-form">
                  <input
                    type="text"
                    name="newMessage"
                    className="message-input"
                    placeholder="Type your message and hit ENTER to send"
                  />
                </form>
              </footer>
            </section>
            <aside className="sidebar right-sidebar">
              {showLogin ? (
              <Dialog
                userId={userId}
                handleInput={this.handleInput}
                connectToChatkit={this.connectToChatkit}
              />
              ) : null}
            </aside>
          </div>
        );
      }
    }

    export default App;