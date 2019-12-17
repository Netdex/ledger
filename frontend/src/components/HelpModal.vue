<template>
    <b-modal id="help-modal"
             title="Help"
             size="lg"
             lazy>
        <b-container fluid>
            <h5>Abstract</h5>
            <p>
                Ledger allows you to manage IOUs between a group of people using a centralized ledger. With this paradigm, 
                each person is assigned an account in the ledger. The ledger consists of a series of transactions, each 
                either takes (credits) or gives (debits) money into separate accounts.</p>
            <p>
                To simplify this process we add an account called the 'ledger' account. Instead of owing/being owed money 
                from each other, everyone owes/is owed money from the ledger account. For example, if I owe you $50, then this 
                is equivalent to me owing the ledger account $50, and the ledger account owing you $50. The result is that 
                everyone is either is owed by/owes money to a single account. The ledger account must always have a balance 
                of $0, since its debits must match its credits.</p>
            <p>
                When it is time to reconcile the ledger, all that is needed to be done is for accounts which owe the ledger 
                to pay any account which is owed by the ledger. The ledger remains at a $0 balance, and the accounts are 
                reconciled.</p>
            <p>
                With this paradigm it is not important who owes who money - you can pay anyone as long as it balances the ledger. </p>
            <hr>
            <h5>Ledger View</h5>
            <b-img src="https://i.imgur.com/N2N3vGy.png" class="my-4" fluid/>
            <p>
                The Ledger View shows all transactions that have been posted to the ledger, as well as the status 
                of all accounts that have been mentioned in the ledger.</p>
            <p>
                The account view (1) shows the current totals of every account that has been mentioned in the 
                ledger. Accounts with a green total are owed money by the ledger, while accounts with a red total 
                owe money to the ledger. Clicking on an a red total automatically generates a transaction that 
                reconciles that account.</p>
            <p>
                In the ledger table, each row corresponds to a single transaction (2). Each transaction is summarized 
                by the affected accounts, explanation, and date. Pressing the Edit (3) button will allow you to modify 
                the original transaction.</p>
            <hr>
            <h5>Transaction Editor</h5>
            <b-img src="https://i.imgur.com/fbzAS3Q.png" class="my-4" fluid/>

            <p>
                The transaction editor allows you to easily create a transaction affecting multiple accounts. Each 
                transaction consists of a reason, date of occurrence, and a list of debits and credits. The total 
                debits and credits (1) must balance for each transaction to maintain the zero-sum nature of the ledger.</p>
            <p>
                You may click the add button in a debit/credit list to add an entry to the debit/credit list. Each account has a 
                currency input (2) which has three different modes: <b>exact</b>, <b>percent</b>, and <b>balance</b>.
            </p>
            <h6>Exact Mode</h6>
            <p>Exact mode allows you to enter a fixed amount to debit/credit the specified account.</p>

            <h6>Percent Mode</h6>
            <p>
                Percent mode applies a debit/credit on the specified account as a percentage of the opposite credit/debit 
                total. For example, if you have a $50 total of debits, a percentage of 50% in the credits list would amount to 
                a $25 credit on that account. Percent mode can only be enabled on a single list, and is incompatible with 
                balance mode on the opposite list.</p>
            <h6>Balance Mode</h6>
            <p>
                Balance mode automatically calculates a debit/credit such that the total debits equals the total credits. 
                Balance mode can only be applied on a single entry, and is incompatible with percent mode on the opposite 
                list.</p>
        </b-container>
    </b-modal>
</template>