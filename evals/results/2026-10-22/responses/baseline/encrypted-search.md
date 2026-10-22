The requirements conflict. If only end-user devices hold decryption keys, server workers cannot extract plaintext mentions, build a plaintext search index, or inspect every message to generate previews. Providing those workers plaintext or keys changes the confidentiality promise. Encryption at rest or a server-operated enclave does not by itself preserve the stated boundary that servers cannot read plaintext.

Use an established, audited end-to-end messaging protocol and its supported multi-device design. Devices encrypt messages; servers authenticate users, enforce conversation membership, route ciphertext, and retain encrypted history according to policy. Servers still observe some metadata, such as routing identifiers and timing; document that separately from message-content confidentiality.

Move content features onto authorized devices:

- Decrypt and index messages locally for full-text search. A new device's search completeness depends on which history it securely receives.
- Parse mentions on the sender or recipient device. Encrypt mention content with the message. If the product requires server-targeted mention notifications, explicitly disclose the limited metadata supplied to the server and its privacy implications.
- Generate link previews on a client and include the preview inside the encrypted message. Fetching links reveals information to the destination and can create tracking risks, so make fetching deliberate and restrict unsafe targets. A server preview proxy would learn the submitted URL, even if it never receives the rest of the message; that is a deliberate relaxation, not invisible E2EE behavior.

Encrypt media on the client with fresh content keys using the established protocol's attachment mechanism. Upload encrypted blobs to private storage, and send the media key and integrity information inside the encrypted message. Downloads are authorized and decrypted locally. Server malware scanning, thumbnail generation, and media recognition cannot inspect plaintext under this design; perform suitable processing on devices or revise those requirements.

Adding a second device requires authenticated enrollment through the protocol's supported device-linking or recovery mechanism. Existing trusted devices can securely transfer history and keys, or an end-to-end encrypted backup can restore them. Decide explicitly whether the new device can read historical messages. Future messages must include the new authorized device according to the protocol; revocation stops future access but cannot erase material already decrypted by that device.

If server-side plaintext indexing and extraction are mandatory, change the product claim and key-access architecture accordingly. Do not claim both exclusive endpoint access and universal server plaintext processing.
