package pokemons93055.move.physical;

import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Status;
import ru.ifmo.se.pokemon.Stat;
import ru.ifmo.se.pokemon.PhysicalMove;
import ru.ifmo.se.pokemon.Type;

/**
 * Defines a new physical move - Facade. It deals
 * damage and hits with double power (140) if the user 
 * is burned, poisoned or paralyzed.
 * 
 * In the case of a burn, the usual attack-halving still 
 * occurs so Facade hits with an effective power of 70.
 * 
 * @author developer
 */
public class Facade extends PhysicalMove {
    
    private static final double POWER = 70;
    private static final double ACCURACY = 100;
    
    public Facade() {
        super(Type.FAIRY, POWER, ACCURACY);
    }
    
    @Override protected double calcBaseDamage(Pokemon attacker, Pokemon defender) {
        double damage = super.calcBaseDamage(attacker, defender);
        
        Status defenderStatus = defender.getCondition();
        
        // Increasing attack if these conditions are followed:
        if (defenderStatus.equals(Status.BURN) || 
            defenderStatus.equals(Status.POISON) ||
            defenderStatus.equals(Status.PARALYZE)) {
            damage *= 2;
        }
        
        return damage;
    }
    
    @Override protected String describe() {
        return "uses Facade!";
    }
}
