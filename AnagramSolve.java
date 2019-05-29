import java.util.*;
import java.io.*;

		

public class AnagramSolve{


	static String[] arr = new String[100000];

	static int m = 0;

	
	public static void main(String[] args) throws Exception {

//Map�̍쐬

		Map<String,String> map1 = new HashMap<String,String>();


 		String[] strArray1 = new String[100000];

		String[] strArray2 = new String[100000];
      
 		int i = 0;
       
       
 		try{

			File file = new File("LowerSortDictionary.txt");

			BufferedReader br = new BufferedReader(new FileReader(file));

			String str= null;

			i=0;

			while((str = br.readLine()) != null){


				strArray1[i] = str;

				i++;

              
			}
		
			br.close();



		}
		catch(FileNotFoundException e){
        		System.out.println(e);
		}
		catch(IOException e){
        		System.out.println(e);
		}



 		try{

			File file = new File("LowerDictionary.txt");

			BufferedReader br = new BufferedReader(new FileReader(file));

			String str= null;

			i=0;

			while((str = br.readLine()) != null){


				strArray2[i] = str;

				i++;

              
			}
		
			br.close();



		}
		catch(FileNotFoundException e){
        		System.out.println(e);
		}
		catch(IOException e){
        		System.out.println(e);
		}







		for(int k=0; k<72412; k++){

			map1.put(strArray1[k],strArray2[k]);

		}

//Scan,Sort,Combine,


		String[] copyArr = new String[100000];

		int[] countArr = new int[100000];



		Scanner scan = new Scanner(System.in);

		String strIn = scan.next();

		char[] charArr = strIn.toCharArray(); 

		Arrays.sort(charArr);


		String ans = new String(charArr);


		combine(ans, new StringBuffer(), 0);
//Search map1

		int b = 0;

		for (int a=0; a<m; a++){
		
			if(map1.get(arr[a]) != null){

				copyArr[b] = arr[a];


				b++;
			}	

		}


		int max = 0;

		int maxNum = 0;

		for(int num = 0; num<b+1; num++){

			char[] charCopyArr = copyArr[num].toCharArray();

			int counter = 0;

			for(int num2 = 0; num2<copyArr[num].length(); num2++){


				switch (charCopyArr[num2]){

				case 'a':
				case 'b':
				case 'd':
				case 'e':
				case 'g':
				case 'i':
				case 'n':
				case 'o':
				case 'r':
				case 's':
				case 't':
				case 'u':
					counter = counter + 1;

					break;

				case 'c':
				case 'f':
				case 'h':
				case 'l':
				case 'm':
				case 'p':
				case 'v':
				case 'w':
				case 'y':
					counter = counter + 2;

					break;

				case 'j':
				case 'k':
				case 'q':
				case 'x':
				case 'z':
					counter = counter + 3;

					break;

				}
			}

			countArr[num] = counter;

	
			if(max < countArr[num]){

				max = countArr[num];

				maxNum = num;

				System.out.println(maxNum+","+copyArr[maxNum]+","+map1.get(copyArr[maxNum])+","+max);
		
			}
	
		}	

	}


	private static void combine(String instr, StringBuffer outstr, int index){

		for (int k = index; k < instr.length(); k++){

			outstr.append(instr.charAt(k));

			if(outstr.length() > 2){

				arr[m] = outstr.toString();
				m++;

			}
			
			combine(instr, outstr, k + 1);

			outstr.deleteCharAt(outstr.length() - 1);

		}

	} 


}
	









