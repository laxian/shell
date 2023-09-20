package src;

import java.nio.charset.StandardCharsets;

/**
 * @author ljf94
 */
public class Aes extends AbstractAes256 {

    /**
     * Encrypt text with the passphrase
     *
     * @param input      Input text to encrypt
     * @param passphrase The passphrase
     * @return A base64 encoded string containing the encrypted data
     * @throws Exception Throws exceptions
     */
    public static String encrypt(String input, String passphrase) throws Exception {
        return java.util.Base64.getEncoder().encodeToString(
                _encrypt(input.getBytes(StandardCharsets.UTF_8), passphrase.getBytes(StandardCharsets.UTF_8)));
    }

    /**
     * Encrypt text in bytes with the passphrase
     *
     * @param input      Input data in bytes to encrypt
     * @param passphrase The passphrase in bytes
     * @return A base64 encoded bytes containing the encrypted data
     * @throws Exception Throws exceptions
     */
    public static byte[] encrypt(byte[] input, byte[] passphrase) throws Exception {
        return java.util.Base64.getEncoder().encode(_encrypt(input, passphrase));
    }

    /**
     * Decrypt encrypted base64 encoded text in bytes
     *
     * @param crypted    Text in bytes to decrypt
     * @param passphrase The passphrase in bytes
     * @return Decrypted data in bytes
     * @throws Exception Throws exceptions
     */
    public static String decrypt(String crypted, String passphrase) throws Exception {
        return new String(
                _decrypt(java.util.Base64.getDecoder().decode(crypted), passphrase.getBytes(StandardCharsets.UTF_8)),
                StandardCharsets.UTF_8);
    }

    /**
     * Decrypt encrypted base64 encoded text in bytes
     *
     * @param crypted    Text in bytes to decrypt
     * @param passphrase The passphrase in bytes
     * @return Decrypted data in bytes
     * @throws Exception Throws exceptions
     */
    public static byte[] decrypt(byte[] crypted, byte[] passphrase) throws Exception {
        return _decrypt(java.util.Base64.getDecoder().decode(crypted), passphrase);
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 3) {
            System.out.println("Usage: java -jar aes.jar <text> <key> <encrypt|decrypt>");
        }
        String enc = args[0];
        String key = args[1];
        String method = args[2];
        if (method.equals("encrypt")) {
            System.out.println(encrypt(enc, key));
        } else if (method.equals("decrypt")) {
            System.out.println(decrypt(enc, key));
        } else {
            System.out.println("Invalid method");
        }
        // String key = "c12307371ee1490e";
        // String enc = "{\"command\":\"settings get secure
        // robot_id\",\"downloadKey\":\"\"}";
        // String encrypt = encrypt(enc, key);
        // System.out.println(encrypt);
        // String decrypt = decrypt(
        // "cGFyYW1zdHKasy027tCVjLGDUnQDvN/rw0WWFMLgn9fMe8PYWUUGwdISIA3Dfk16Fm1ZMShS88Ti9WgV3yKrV4QYHWMD0imwlhWpqCMFqfE=",
        // key);
        // String decrypt2 = decrypt(
        // "cGFyYW1zdHII3KUhzKLNpK3+JSGhgghGg1et/mFdhm6WcpwOjdYjTtxAyF/f1LT7wrn2E7v1+Wrycv8MpfjtZ0agElVI50Ap0HdVO1mCzUI=",
        // key);
        // String decrypt3 = decrypt(
        // "cGFyYW1zdHJRJPO8p31aTYKU1kgKJCwgo4zIusGluRyfcMjBi0HZUQbqNWquRHC4FRsvT71hwPS2diAqJF9RPHsGq1ojDCjUv/IEk5eJPmA=",
        // key);
        // System.out.println(decrypt);
        // System.out.println(decrypt2);
        // System.out.println(decrypt3);
    }
}
