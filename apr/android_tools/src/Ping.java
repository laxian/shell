package src;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Ping {
    public static void main(String[] args) {
        if (args.length == 0) {
            System.out.println("请提供IP地址作为参数！");
            return;
        }

        String ipAddress = args[0];
        System.out.println("正在 Ping " + ipAddress + " ...");

        try {
            ProcessBuilder processBuilder;
            if (System.getProperty("os.name").startsWith("Windows")) {
                processBuilder = new ProcessBuilder("ping", "-n", "5", ipAddress);
            } else {
                processBuilder = new ProcessBuilder("ping", "-c", "5", ipAddress);
            }

            Process process = processBuilder.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }

            int exitCode = process.waitFor();
            System.out.println("\nPing 完成！退出码: " + exitCode);

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
