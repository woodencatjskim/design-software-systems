These requirements conflict. Workers cannot extract arbitrary mentions, build plaintext full-text indexes, or inspect message links while the server is unable to read plaintext. Giving workers decryption keys changes the end-to-end encryption trust boundary.

Assume preserving E2EE is the priority. Use a vetted E2EE protocol and maintained implementation appropriate to multi-device group messaging; do not invent cryptography.

```text
Sender device: parse/search metadata, encrypt
        → server: ciphertext storage and routing
        → recipient devices: decrypt, index, display
```

Parse mentions on the sender or recipient device. Put rich mention information inside the encrypted message. If mention-specific server push is necessary, clients can explicitly submit minimal routing identifiers, but this leaks who was mentioned. Treat that as an explicit privacy decision. Otherwise send generic encrypted-message notifications and resolve mentions locally.

Maintain full-text indexes locally after decryption. Each authorized device can download permitted ciphertext history and build its own index. This costs device storage, CPU, and initial synchronization time. Server-side encrypted search is not a drop-in replacement for plaintext full-text search and has substantial functionality and leakage trade-offs; avoid making it a baseline dependency.

Generate previews on a client and include the preview in encrypted content. Automatic fetching can disclose the user's IP or viewing behavior to linked sites, so provide appropriate controls. A server preview proxy would learn the supplied URLs even if it never sees the full message. If chosen, disclose that relaxation and defend the proxy against unsafe destinations, redirects, and excessive responses. It does not satisfy strict concealment of message URLs from the service.

Encrypt media on the sending device with keys managed by the established protocol, upload ciphertext to private object storage, and transmit media keys and integrity information inside encrypted messages. Download authorization still matters even for ciphertext. Servers cannot generate plaintext thumbnails, transcode content, or scan its plaintext; clients must perform those operations or the privacy requirement must change. Object size, traffic timing, and routing metadata may remain observable.

Enroll a second device using the protocol's authenticated device-linking process. Users must be able to verify and revoke devices. History availability requires an explicitly supported encrypted history transfer or backup scheme; adding a device does not automatically give it old keys. The server must not silently add devices that receive plaintext keys. Revocation protects future access, not plaintext already downloaded.

If server plaintext indexing and extraction are mandatory, change the encryption promise to permit server processing and state that clearly. Revisit local index size, synchronization cost, device recovery usability, and metadata exposure as usage grows.
