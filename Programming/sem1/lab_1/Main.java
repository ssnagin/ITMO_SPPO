public class Main {
        
	public static void main(String[] args) {

            /* 
            
            Некоторые комментарии о лабе:
            
            - дедлайн до след. лабы!!!            
            - вариант 31525,
            - w[i] -- это к 1 массиву

            */
            
            long[] w = new long[11];
            int value = 6;
            
            double lowerRange = -6;
            double upperRange = 10;
            
            float[] x = new float[15];
            
            double result[][] = new double[11][15];
            double currentValue;
            
            // Set values for w:
            for (int i = 0; i < w.length; i++) {
                w[i] = value;
                value++;
            }
            
            // Set values for x:
            for (int i = 0; i < x.length; i++) {
                x[i] = (float) (lowerRange + Math.random() * (upperRange - lowerRange));
            }
            
            // Set values for mega-super-two-dimentional array "result":
            for (int i = 0; i < result.length; i++) {
                for (int j = 0; j < result[i].length; j++) {
                    currentValue = (double) x[j];
                    result[i][j] = nextElement(currentValue, w[i]);
                }
            }
            
            // Print all elements into console:
            print(result);
	}
        
        /*
        
        Считает след. элемент массива на основе входных данных:
        
        double x                рандомное значение x из подготовленных значений в
                                float[15] x
        long wArrayValue        Элемент из массива w (main)
        
        */
        
        public static double nextElement(double x, long wArrayValue) {
            
            int[] secondGroupNumbers = {6,7,10,12,14};
            
            // The 1st group (w == 16):
            if (wArrayValue == 16) {
                return Math.sin((3.0/4.0) * 
                        Math.pow(x, (x/2.0) ));
            }
            
            // w_value ∈ {6, 7, 10, 12, 14} condition (2nd group):
            for (int k = 0; k < secondGroupNumbers.length; k++) {
                if (secondGroupNumbers[k] != wArrayValue) continue;
                return Math.cos(Math.tan(Math.pow(Math.E, x)));
            }
            
            // Other values (3rd group):
            return Math.log10(Math.pow(Math.sin(
                    Math.asin( (x + 2.0) / 16.0 )
            ), 2.0));
        }
        
        /*
        
        Выводит на экран двумерный массив
        
        double[][] matrix       массив, который необходимо вывести
        
        */
        public static void print(double[][] matrix) {
            String row = "";
            for (int i = 0; i < matrix.length; i++) {
                for (int j = 0; j < matrix[i].length; j++) {
                    row += String.format("8.4f", matrix[i][j]) + " ";
                }
                row += "\n";
            }
            System.out.print(row);
        }
}