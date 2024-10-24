use tungstenite::{connect, Message};
use url::Url;

fn main() {
    let (mut socket, response) = connect(Url::parse("ws://localhost:6789").unwrap())
        .expect("Can't connect");
    println!("Connected to the server: {}", response.status());

    // Sending a message
    socket.write_message(Message::Text("Hello from Rust!".into()))
        .expect("Failed to send message");

    // Receiving a message
    loop {
        let msg = socket.read_message().expect("Failed to read message");
        match msg {
            Message::Text(text) => println!("Received: {}", text),
            Message::Close(_) => {
                println!("Connection closed by server");
                break;
            },
            _ => (),
        }
    }
}
