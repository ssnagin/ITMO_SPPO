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
            double ww[][] = new double[11][15];
            double current_x;
            
            int[] numbers = {6,7,10,12,14};
            
            for (int i = 0; i < ww.length; i++) {
                for (int j = 0; j < ww[i].length; j++) {
                    
                    current_x = (double) x[j];
                    
                    // ww[i] == 16 condition (1st group):
                    if (w[i] == 16) {
                        ww[i][j] = Math.sin((3.0/4.0) * Math.pow(current_x, (current_x/2.0) ));
                        continue;
//                        System.out.println(ww[i][j]);
                    }
                    
                    // w[i] ∈ {6, 7, 10, 12, 14} condition (2nd group):
                    for (int k = 0; k < numbers.length; k++) {
                        if (!(w[i] == numbers[k])) {
                            // Other values (3rd group):
                            ww[i][j] = Math.log10(Math.pow(Math.sin(Math.asin( (current_x + 2.0) / 16.0 )), 2.0));
                            System.out.println(w[i] + " " + ww[i][j]);
                        }
                        ww[i][j] = Math.cos(Math.tan(Math.pow(Math.E, current_x)));
//                        System.out.println(w[i] + " " + ww[i][j]);
                    } 
                }
            }
	}
}
