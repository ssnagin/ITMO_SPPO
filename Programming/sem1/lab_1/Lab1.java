class Lab1 {
        
	public static void main(String[] args) {

            /* 
            
            Некоторые комментарии о лабе:
            
            - дедлайн до след. лабы!!!            
            - вариант 31525,
            - w[i] -- это к 1 массиву

            */
            
            long[] w = new long[11];
            int value = 6;
            
            double min_ = -6;
            double max_ = 10;
            
            float[] x = new float[15];
            
            double result[][] = new double[11][15];
            double current_x;
            
            // Set values for w:
            for (int i = 0; i < w.length; i++) {
                w[i] = value;
                value++;
            }
            
            // Set values for x:
            for (int i = 0; i < x.length; i++) {
                x[i] = (float) (min_ + Math.random() * (max_ - min_));
            }
            
            // Set values for mega-super-two-dimentional array "result":
            for (int i = 0; i < result.length; i++) {
                for (int j = 0; j < result[i].length; j++) {
                    current_x = (double) x[j];
                    result[i][j] = nextElement(current_x, w[i]);
                }
            }
            
            // Print all elements into console:
            print(result);
	}
        
        /*
        
        Считает след. элемент массива на основе входных данных:
        
        double current_x        рандомное значение x из подготовленных значений в
                                float[15] x
        
        */
        
        public static double nextElement(double current_x, long w_value) {
            
            int[] NUMBERS = {6,7,10,12,14};
            
            // The 1st group (w == 16):
            if (w_value == 16) {
                return Math.sin((3.0/4.0) * 
                        Math.pow(current_x, (current_x/2.0) ));
            }
            
            // w_value ∈ {6, 7, 10, 12, 14} condition (2nd group):
            for (int k = 0; k < NUMBERS.length; k++) {
                if (NUMBERS[k] != w_value) continue;
                return Math.cos(Math.tan(Math.pow(Math.E, current_x)));
            }
            
            // Other values (3rd group):
            return Math.log10(Math.pow(Math.sin(
                    Math.asin( (current_x + 2.0) / 16.0 )
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
                    Double formatting_num = matrix[i][j];
                    row += round(formatting_num, 4) + " ";
                    if (formatting_num >= 0) row += " ";
                }
                row += "\n";
            }
            System.out.print(row);
        }
        
        /*
        
        Округляет (нормально) до n-цифры после запятой
        
        double value        значение, которое нужно округлить
        int places          до какой n-ой цифры нужно округлить
        
        */
        public static double round(double value, int places) {
            double scale = Math.pow(10, places);
            return Math.round(value * scale) / scale;
        }
}