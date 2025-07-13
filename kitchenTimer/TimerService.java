public class TimerService {
    public static void main(String[] args) throws InterruptedException {
        int seconds = Integer.parseInt(args[0]);
        while (seconds > 0) {
            System.out.println("残り秒数: " + seconds);
            Thread.sleep(1000);
            seconds--;
        }
        System.out.println("TIME_UP");
    }
}
