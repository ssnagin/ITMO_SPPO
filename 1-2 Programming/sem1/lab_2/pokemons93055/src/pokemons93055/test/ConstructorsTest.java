package pokemons93055.test;

/**
 *
 * @author developer
 */

public class ConstructorsTest {
    
    int a,b,c;
    
    public ConstructorsTest(int a, int b) {
        this.a = a;
        this.b = b;
        // this(a,b); // это не пройлдет через компилятор
    }
    
    public ConstructorsTest(int a, int b, int c) {
        this(a, b);
        this.c = c;
    }
   
    
    // При вызове new ConstructorsTest(1,2,3) (20) сначала
    // обработается this(1,2), потом this.c
    // При вызове new Constructor(1,2) вызывается (15) this.a и this.b
    
    /*
    В java можно вызывать конструктор родительского класса ровно 1 раз, в рамках вызова конструктора 
    дочернего класса. Для каждого уровня иерархии конструктор вызывается только для инициализации дочернего 
    */
}