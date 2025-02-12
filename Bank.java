import java.util.*;

/////////////////   نظام اداره بنك ////////////////////////////////
public class Bank {
 ArrayList<Account> accounts;
 
     public Bank() {
         this.accounts = new ArrayList<>();
     }
     public void addAccount(Account account) {
         accounts.add(account); 
     }
     
     Account findAccount(String accountNumber){
         for (Account  account: accounts){
             if(account.getAccountNumber().equals(accountNumber)){
                 return account;
             }
         } return  null;
     }
 
      void printAllAccount(){
             for(Account account :accounts){
                 System.out.println(account.getAccountDetails());
             }
         }
         public static  void main(String[] args) {
     
             Bank bankCib =new Bank();
             Scanner scanner = new Scanner(System.in);
            Administrator admin = new Administrator("Yahia", "Sugar", 512, bankCib);
            
                 while (true){
                     System.out.println("\n1.open Account \n2.Deposit \n3.Withdraw \n4.AccountDetails\n5.printAllAccount history\n6.administrator  \n7.Exit");
                     System.out.println("Enter YOUR Choice ");
                      int choice = scanner.nextInt();
                      switch (choice) {
                         case 1:
                             System.out.println("ENTER Account type(Saving, Current)");
                             String type = scanner.next();
                             System.out.println("Enter Account name ");
                             String name = scanner.next();
                             System.out.println("enter initial balance");
                             double balance = scanner.nextDouble();
                             System.out.println("Enter password");
                             int accountPassword = scanner.nextInt();
                             if (type.equalsIgnoreCase("Saving")) {
                                 SavingsAccount savingsAccount = new SavingsAccount(name, "SAV" + (bankCib.accounts.size() + 1), balance, 14, accountPassword);
                                 System.out.println("Account created successfully");
                                 savingsAccount.generateAccountNumber();
                                 bankCib.addAccount(savingsAccount);
                                 // after creating account apply monthly update after 30 days
                                 if (new Date().getDate() == 30) {
                                     savingsAccount.applyMonthlyUpdate();
                                 }
                                 System.out.println(savingsAccount.getAccountDetails());

                             } else if(type.equalsIgnoreCase("Current")) {
                                CurrentAccount currentAccount = new CurrentAccount(name, "CUR" + (bankCib.accounts.size() + 1), balance, accountPassword);
                                 bankCib.addAccount(currentAccount);
                                 System.out.println("Account created successfully");
                                 currentAccount.generateAccountNumber();
                                 System.out.println(currentAccount.getAccountDetails());
                             }
                                else {
                                    System.out.println("Invalid account type");
                                }
                             break;
     
                             case 2:
                                 System.out.println("Enter Account Number");
                                 String accountNumber = scanner.next();
                                 Account account = bankCib.findAccount(accountNumber);
                                 if(account != null){
                                     System.out.println("Enter amount to deposit");
                                     double amount = scanner.nextDouble();
                                     System.out.println("Enter password");
                                     int DepositPassword = scanner.nextInt();
                                     account.deposit(amount, DepositPassword);
                                     Transactions DepositTransactions = new Transactions("Deposit", new Date(), amount);
                                     System.out.println("Deposit successful");
                                     System.out.println(account.getAccountDetails());
                                 
                                 }else {
                                     System.out.println("Account not found");
                                 }
                                 break;
                             case 3:
                                   System.out.println("Enter Account Number");
                                 String accountNumber1 = scanner.next();
                                 Account account1 = bankCib.findAccount(accountNumber1);
                                 if(account1!=null){
                                     System.out.println("Enter amount to withdraw");
                                     double amount = scanner.nextDouble();
                                     System.out.println("Enter password");
                                     int withdrawPassword = scanner.nextInt();
                                     account1.withdraw(amount, withdrawPassword);
                                     Transactions withdrawTransactions = new Transactions("Withdraw", new Date(), amount);
                                     System.out.println("Withdraw successful");
                                     System.out.println(account1.getAccountDetails()); 
                                 }else {
                                     System.out.println("Account not found");
                                 }
                                 break;
                             case 4:
                                 System.out.println("Enter Account Number");
                                 String accountNumber2 = scanner.next();
                                 Account account2 = bankCib.findAccount(accountNumber2);
                                 if(account2!=null){
                                     System.out.println("Enter password");
                                     int accountPassword1 = scanner.nextInt();
                                     if(account2.checkPassword(accountPassword1)){
                                         System.out.println(account2.getAccountDetails());
                                     }else {
                                         System.out.println("Invalid password");
                                     }
                                 }else {
                                     System.out.println("Account not found");
                                 }
                                 break;
                             case 5:
                                 System.out.println("Enter Account Number");
                                 String accountNumber3 = scanner.next();
                                 Account account3 = bankCib.findAccount(accountNumber3);
                                 if(account3!=null){
                                     System.out.println("Enter password");
                                     int accountPassword2 = scanner.nextInt();
                                     if(account3.checkPassword(accountPassword2)){
                                         account3.printTransactions();
                                     }}else {
                                         System.out.println("Invalid password");
                                     }
                                     break;
                             case 6:
                                        System.out.println("Enter admin name");
                                        String adminName = scanner.next();
                                        System.out.println("Enter admin password");
                                        String adminPassword = scanner.next();
                                        System.out.println("Enter admin id");
                                        int adminId = scanner.nextInt();
                                    
                                        if (adminName.equals(admin.name) && adminPassword.equals(admin.password) && adminId == admin.id) {
                                            System.out.println("1. Show All Accounts");
                                            int adminChoice = scanner.nextInt();
                                            if (adminChoice == 1) {
                                                admin.printAllAccounts();  // Correctly prints all accounts
                                            }
                                        } else {
                                            System.out.println("Invalid admin name, password, or ID.");
                                        }
                                        break;
                                       
                                    case 7:
                                        System.exit(0);
                                        break;
                                   default:
                                        System.out.println("Invalid choice");
                                        break;
                                
    
                     }
                    
                }
            }
    }



  abstract class Account {
    String accountHolderName;
    String accountNumber ;
    double balance;
    int password;
   ArrayList <Transactions>transactions ;

    public Account(String accountHolderName, String accountNumber, double balance, int password) {
        this.accountHolderName = accountHolderName;
        this.accountNumber = accountNumber;
        this.balance = balance;
        this.transactions =new ArrayList<>() ;
        this.password = password;
    }

    public String getAccountHolderName() {
        return accountHolderName;
    }


    public String getAccountNumber() {
        return accountNumber;
    }


    public double getBalance() {
        return balance;
    }
    public int getPassword() {
        return password;
    }
    public boolean checkPassword(int password){
        return  this.password == password;
    }


    void deposit(double amount,int password){
        if(amount >0 && checkPassword(password)){
            balance+=amount;
            transactions.add(new Transactions ("Deposit", new Date(), amount));
        } else {
            System.out.println("Invalid deposit amount or password");
        }
    }

    boolean withdraw(double amount,int password){
        if(amount> 0 && amount <= balance&& checkPassword(password)){
            balance -=amount;
            transactions.add(new Transactions("Withdraw", new Date(), amount));
            return  true;
        }
        else {
            System.out.println("invalid amount or password");
            return  false;
        }
    }

    void printTransactions(){
        System.out.println("Transaction history for Account " + accountNumber);
        for (Transactions transactions1 : transactions){
            System.out.println(transactions1);
        }
    }

    String getAccountDetails(){
        return  "AccountNumber : "+ accountNumber +"\n AccountHolder : " + accountHolderName + "\nBalance : " +balance;
    }

    abstract  void applyMonthlyUpdate();
    //randome number for account number
    public String generateAccountNumber(){
            return  UUID.randomUUID().toString();
        }
    
    }
    
    
    class Transactions{
        String type;
        Date date ;
        double amount ;
    
        public Transactions(String type, Date date, double amount) {
            this.type = type;
            this.date = date;
            this.amount = amount;
        }
        
        
            @Override
            public String toString() {
                return "Type: " + type + ", Date: " + date + ", Amount: " + amount;
            }
        }
    
    
    class SavingsAccount extends Account{
    double interestRate=14;
        public SavingsAccount(String accountHolderName, String accountNumber, double balance , double interestRate,int password) {
            super(accountHolderName, accountNumber, balance,password);
            this.interestRate = interestRate;
        }
    
        @Override
        void applyMonthlyUpdate() {
            balance+=(balance *interestRate /100);
        }

        @Override
        String  getAccountDetails(){
            return  super.getAccountDetails() + "\nInterest Rate : " + interestRate+ "%";
    
        }

        @Override
        public String generateAccountNumber(){
            this.accountNumber = "SAV" + (int)(Math.random()*1000);
            return accountNumber;
        }
        

}
     class CurrentAccount extends Account{
        public CurrentAccount(String accountHolderName, String accountNumber, double balance, int password) {
            super(accountHolderName, accountNumber, balance, password);
        }

        @Override
        void applyMonthlyUpdate() {
            balance=balance;
        }

        @Override
        public String generateAccountNumber(){
             this.accountNumber = "CUR" + (int)(Math.random()*1000);
             return accountNumber;
}  
}
    
class Administrator {

    String name;
    String password;
    int id;
    Bank bank;  // Reference to Bank instance

    public Administrator(String name, String password, int id, Bank bank) {
        this.name = name;
        this.password = password;
        this.id = id;
        this.bank = bank;  // Store reference to Bank
    }

    void printAllAccounts() {
        if (bank.accounts.isEmpty()) {
            System.out.println("No accounts available.");
        } else {
            for (Account account : bank.accounts) {
                System.out.println(account.getAccountDetails());
            }
        }
    }
}
