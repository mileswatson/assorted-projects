import java.math.BigInteger;
import java.security.*;
import java.util.Random;

public class Crypter {
	
	public String encryptString(String str, String encryptKey, String sharedKey) {
		BigInteger encryptKeyBig = new BigInteger(encryptKey,16);
		BigInteger sharedKeyBig = new BigInteger(sharedKey,16);
		char[] charList = str.toCharArray();
		String returnString = "";
		BigInteger x;
		for(int i=0;i<charList.length;i++) {
			x = new BigInteger(Integer.toString((int) charList[i]));
			x = x.add(BigInteger.valueOf(i+1));
			x = x.modPow(encryptKeyBig, sharedKeyBig);
			returnString += x.toString(16) + " ";
		}
		return returnString.substring(0, returnString.length()-1);
	}

	public String decryptString(String str, String decryptKey, String sharedKey) {
		BigInteger decryptKeyBig = new BigInteger(decryptKey,16);
		BigInteger sharedKeyBig = new BigInteger(sharedKey,16);
		String[] stringList = str.split(" ");
		String returnString = "";
		BigInteger x;
		for (int i = 0; i < stringList.length; i++) {
			x = new BigInteger(stringList[i],16);
			x = x.modPow(decryptKeyBig,sharedKeyBig);
			x = x.subtract(BigInteger.valueOf(i+1));
			returnString += (char) x.intValue();
		}
		return returnString;
	}
	
	public String[] getKeys(int strength) {
		BigInteger aPrime = getPrime(Crypter.randomHex(strength));
		BigInteger bPrime = getPrime(Crypter.randomHex(strength));
		BigInteger n = aPrime.multiply(bPrime);
		BigInteger totientN = aPrime.subtract(BigInteger.ONE).multiply(bPrime.subtract(BigInteger.ONE));
		BigInteger e;
		do {
			e = getPrime(Crypter.randomHex(strength));
		} while ((e.compareTo(n) > -1) || (n.mod(e).compareTo(BigInteger.ZERO) == 0));
		BigInteger d = new BigInteger("1");
		try {
  		while (true) {
  			if (e.multiply(d).subtract(BigInteger.ONE).mod(totientN).compareTo(BigInteger.ZERO) == 0) {
  				System.out.println(e.multiply(d).subtract(BigInteger.ONE).mod(totientN));
  				break;
  			} else {
  				d = d.add(BigInteger.ONE);
  			}
  		}
		} catch (Throwable ex) {
      System.out.println(ex.toString());
		}
		String[] returnList = new String[3];
		returnList[0] = e.toString(16);
		returnList[1] = n.toString(16);
		returnList[2] = d.toString(16);
		return returnList;
	}
	
	public static String randomHex(int length) {
	  String SALTCHARS = "0123456789abcdef";
    StringBuilder salt = new StringBuilder();
    Random rnd = new Random();
    while (salt.length() < length) {
      int index = (int) (rnd.nextFloat() * SALTCHARS.length());
      salt.append(SALTCHARS.charAt(index));
    }
    String saltStr = salt.toString();
    return saltStr;
	}
	
	public BigInteger getPrime(String startNum) {
		BigInteger limit, testFor;
		BigInteger testNum = new BigInteger(startNum,16);
		Boolean prime;
		testNum = testNum.add(testNum.add(BigInteger.ONE).mod(BigInteger.valueOf(2)));
		while(true) {
			limit = roundSqrt(testNum);
			testFor = new BigInteger("3");
			prime = true;
			while (testFor.compareTo(limit)<1) {
				if (testNum.mod(testFor) == BigInteger.ZERO) {
					prime = false;
					break;
				}
				testFor = testFor.add(BigInteger.valueOf(2));
			}
			if (prime) {
				return testNum;
			}
			testNum  = testNum.add(BigInteger.valueOf(2));
		}
		
	}
	
	public BigInteger roundSqrt(BigInteger testNum) {
		BigInteger tryVal = new BigInteger("0");
		while (true) {
			tryVal = tryVal.add(BigInteger.valueOf(1));
			if (tryVal.multiply(tryVal).compareTo(testNum) > -1) {
				return tryVal;
			}
		}
	}
	
	public String getHash(String message, String type) {
		String returnString = "";
		try {
			MessageDigest md = MessageDigest.getInstance("SHA-"+type);
			byte[] hash = md.digest(message.getBytes("UTF-8"));
			StringBuilder sb = new StringBuilder();
			for(byte b: hash) {
				sb.append(String.format("%02X", b));
			}
			returnString = sb.toString();
		}
		catch (Throwable e) {
			e.printStackTrace();
		}
		return returnString;
	}
	
}