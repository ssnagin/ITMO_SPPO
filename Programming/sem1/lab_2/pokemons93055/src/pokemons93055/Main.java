package pokemons93055;

import ru.ifmo.se.pokemon.Battle;
import pokemons93055.pokemons.Celebi;
import pokemons93055.pokemons.Bidoof;
import pokemons93055.pokemons.Bibarel;
import pokemons93055.pokemons.Deino;
import pokemons93055.pokemons.Hydreigon;
import pokemons93055.pokemons.Zweilous;


/**
 *
 * @author developer
 */

/*

Attacks:
- Confusion +
- Magical Leaf +
- Swagger +
- Dazzling Gleam +
- Facade +
- Defense Curl +
- Amnesia +
- Waterfall +
- Focus Energy +?
- Double Hit +?
- Steel Wing +
*/
public class Main {
    
    /**
     * 
     * @param args the command line arguments
     */
    
    public static void main(String[] args) {
        Battle battle = new Battle();
        
        Celebi celebi = new Celebi("Подопытное мясо", 1);
        Bidoof bidoof = new Bidoof("Иван", 1);
        Bibarel bibarel = new Bibarel("Бобер-гигачад", 1);
        Deino deino = new Deino("Бедолага", 1);
        Zweilous zweilous = new Zweilous("Сиамский инвалид", 1);
        Hydreigon hydreigon = new Hydreigon("После бутылки флэша", 1);
        
        // 1st Team:
        battle.addAlly(celebi);
        battle.addAlly(deino);
        battle.addAlly(zweilous);
        
        // 2nd Team:
        battle.addFoe(bidoof);
        battle.addFoe(bibarel);
        battle.addFoe(hydreigon);

        battle.go();
        
//        Celebi celebi = new Celebi("tset", 1);
//
//        Pokemon p2 = new Pokemon("321", 1);
//        
//        battle.addAlly(celebi);
//        battle.addFoe(p2);
//        battle.go();
    }
    
}
