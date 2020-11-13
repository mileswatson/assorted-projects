public class Main {

	public static void main(String args[]) {
		Crypter crypter = new Crypter();
		//System.out.println(crypter.getHash("This string","512"));
		String[] x = crypter.getKeys(3);
		//String[] y = crypter.getKeys("Password04",3);
		//System.out.println(y[0]+" "+y[1]+" "+y[2]);
		System.out.println(x[0]);
	}
	
}