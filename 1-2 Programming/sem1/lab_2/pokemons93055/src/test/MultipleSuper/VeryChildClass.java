package test.MultipleSuper;

import test.MultipleSuper.VeryChildClass;

/**
 *
 * @author developer
 */
public class VeryChildClass extends ChildClass {
    
    public VeryChildClass() {
//        super().super();
        super();
        super.childClassTest();
//        super.super.parentClassTest(); -- ошибка
        System.out.println("VeryChildClass");
    }
}