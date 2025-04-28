package ccc;
import java.util.Scanner;

public class student {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter the number of students in the class: ");
        int numStudents = scanner.nextInt();
        scanner.nextLine(); // consume the leftover newline

        for (int i = 1; i <= numStudents; i++) {
            System.out.print("Enter the name of student " + i + ": ");
            String name = scanner.nextLine(); // use nextLine()

            System.out.print("Enter the average score for " + name + ": ");
            int averageScore = scanner.nextInt();
            scanner.nextLine(); // consume the leftover newline after nextInt()

            char letterGrade;
            if (averageScore >= 90 && averageScore <= 100) {
                letterGrade = 'A';
            } else if (averageScore >= 80 && averageScore < 90) {
                letterGrade = 'B';
            } else if (averageScore >= 70 && averageScore < 80) {
                letterGrade = 'C';
            } else if (averageScore >= 60 && averageScore < 70) {
                letterGrade = 'D';
            } else {
                letterGrade = 'F';
            }

            System.out.println(name + " - Letter Grade: " + letterGrade);
        }

        scanner.close();
    }
}