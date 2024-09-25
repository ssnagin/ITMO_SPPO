class Lab1 {
    
	public static void main(String[] args) {
            
            /* пояснительные комментарии: 
            
            дедлайн до след. лабы!!!            
            Вариант 31525,
            w[i] -- это к 1 массиву

            */
            
            // Set values for w:
            
            long[] w = new long[11];
            int value = 6;
            
            for (int i = 0; i < w.length; i++) {
                w[i] = value;
                value++;
//                System.out.println(w[i]);
            }
            
            // Set values for x:
            
            double min_ = -6;
            double max_ = 10;
            float[] x = new float[15];
            
            for (int i = 0; i < x.length; i++) {
                x[i] = (float) (min_ + Math.random() * (max_ - min_));
//                System.out.println(x[i]);
            }
            
            // Set values for mega-super-two-dimentional array ww:
            double result[][] = new double[11][15];
            double current_x;
         
            for (int i = 0; i < result.length; i++) {
                for (int j = 0; j < result[i].length; j++) {
                    
                    current_x = (double) x[j];
                    
                    result[i][j] = nextElement(current_x, w[i]);
                }
            }
	}
        
        public static double nextElement(double current_x, long w_value) {
            
            int[] NUMBERS = {6,7,10,12,14};
            
            // The 1st group (w == 16)
            if (w_value == 16) return Math.sin((3.0/4.0) * Math.pow(current_x, (current_x/2.0) ));
            
            // w[i] ∈ {6, 7, 10, 12, 14} condition (2nd group):
            for (int k = 0; k < NUMBERS.length; k++) {
                if (NUMBERS[k] != w_value) continue;
                return Math.cos(Math.tan(Math.pow(Math.E, current_x)));
            }
            // Other values (3rd group):
            return Math.log10(Math.pow(Math.sin(Math.asin( (current_x + 2.0) / 16.0 )), 2.0));
        }
}
