/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package test.MultipleSuper;

/**
 *
 * @author developer
 */
public class ChildClass extends ParentClass {
    
    public ChildClass() {
        System.out.println("Child Class");
    }
    
    public void childClassTest() {
        System.out.println("Child Class Test");
    }
    /*
    Super можно вызывать 1 раз тк мы инициализируем 
    цепочку конструкторов от самого старшего по наследованию до 
    текущего дочернего класса. Если вызвать super() более 1 раза 
    то это нарушит логику инициализации классов. Если вызвать super().super(), 
    это нарушает принцип инкапсуляции и приводит к непредсказуемым результатам.
    */
}
