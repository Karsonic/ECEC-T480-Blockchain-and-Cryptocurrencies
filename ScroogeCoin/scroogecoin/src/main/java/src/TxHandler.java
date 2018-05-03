package src;

import java.util.ArrayList;

import src.Transaction.Input;
import src.Transaction.Output;

public class TxHandler {
    
    private UTXOPool pool;

    /**
     * Creates a public ledger whose current UTXOPool (collection of unspent transaction outputs) is
     * {@code utxoPool}. This should make a copy of utxoPool by using the UTXOPool(UTXOPool uPool)
     * constructor.
     */
    public TxHandler(UTXOPool utxoPool) {
        this.pool = new UTXOPool(utxoPool);
    }

    /**
     * @return true if:
     * (1) all outputs claimed by {@code tx} are in the current UTXO pool, 
     * (2) the signatures on each input of {@code tx} are valid, 
     * (3) no UTXO is claimed multiple times by {@code tx},
     * (4) all of {@code tx}s output values are non-negative, and
     * (5) the sum of {@code tx}s input values is greater than or equal to the sum of its output
     *     values; and false otherwise.
     */
    public boolean isValidTx(Transaction tx) {
        UTXOPool unclaimedUTXOPool = new UTXOPool(this.pool);
        ArrayList<Output> txOutputs = tx.getOutputs();
        double inputValue = 0, outputValue = 0;

        // Loop over outputs
        for (int i = 0; i < tx.numOutputs(); i++) {
            UTXO txUTXO = new UTXO(tx.getHash(), i);
            // (1) and (3)
            if (!unclaimedUTXOPool.contains(txUTXO))
                return false;
            // (4)
            if (txOutputs.get(i).value < 0)
                return false;
            
            outputValue += txOutputs.get(i).value;
            unclaimedUTXOPool.removeUTXO(txUTXO);
        }

        // Loop over inputs
        for (int j = 0; j < tx.getInputs().size(); j++) {
            Input input = tx.getInputs().get(j);
            UTXO prevUTXO = new UTXO(input.prevTxHash, input.outputIndex);
            Output prevOutput = this.pool.getTxOutput(prevUTXO);
            
            inputValue += prevOutput.value;

            // (2)
            Crypto.verifySignature(prevOutput.address, tx.getRawDataToSign(j), input.signature);
        }

        // (5)
        if (outputValue > inputValue)
            return false;
    }

    /**
     * Handles each epoch by receiving an unordered array of proposed transactions, checking each
     * transaction for correctness, returning a mutually valid array of accepted transactions, and
     * updating the current UTXO pool as appropriate.
     */
    public Transaction[] handleTxs(Transaction[] possibleTxs) {
        ArrayList<Transaction> validTxs = new ArrayList<>();

        for (Transaction tx: possibleTxs) {
            if(isValidTx(tx)) {
                for (int i = 0; i < tx.numOutputs(); i++) {
                    UTXO txUTXO = new UTXO(tx.getHash(), i);
                    pool.removeUTXO(txUTXO);
                }
                validTxs.add(tx);
            }
        }

        Transaction[] retArray = new Transaction[validTxs.size()];
        return validTxs.toArray(retArray);
    }

}
