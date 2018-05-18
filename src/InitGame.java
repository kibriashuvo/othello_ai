import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Scanner;

public class InitGame {
	String initBoard = "###########........##........##........##...0X...##...X0...##........##........##........###########";

	
	public InitGame() {
		File file = new File("e:\\Othello\\othello_board.txt");	
		file.delete();
		
		file = new File("e:\\Othello\\valid_moves.txt");	
		file.delete();
		
		writeFile("34", "e:\\Othello\\valid_moves.txt");
		writeFile("43", "e:\\Othello\\valid_moves.txt");
		writeFile("56", "e:\\Othello\\valid_moves.txt");
		writeFile("65", "e:\\Othello\\valid_moves.txt");
		writeFile(initBoard, "e:\\Othello\\othello_board.txt");
	
	}
	
	public HashMap<Integer,Integer> textToBoard(){
		Scanner in;
		String board="";
		HashMap<Integer,Integer> map = new HashMap<>();
		
		int w_scr = 0;
		int b_scr = 0;
		try {
			in = new Scanner(new FileReader("e:\\Othello\\othello_board.txt"));
			board = in.nextLine();
		} catch (FileNotFoundException e) {
			
			e.printStackTrace();
		}
		
		
		for(int i=0;i<100;i++){
			if(board.charAt(i)=='#')
				continue;
			else if(board.charAt(i)=='.')
				map.put(i, 0);
			else if(board.charAt(i)=='0'){
				map.put(i, 1);
				w_scr++;
			}				
			else if(board.charAt(i)=='X'){
				map.put(i, 2);
				b_scr++;
			}
				
			
				
		}
		System.out.println("Black= "+b_scr+" White= "+w_scr);
		
		return map;
		
		
		
	}
	
	public static void writeFile(String content,String outputPath){
		
		
		 try{
	          File file =new File(outputPath);
	    	  if(!file.exists()){
	    	 	file.createNewFile();
	    	  }
	    	  FileWriter fw = new FileWriter(file,true);
	    	  BufferedWriter bw = new BufferedWriter(fw);
	    	  PrintWriter pw = new PrintWriter(bw);	         
	    	  pw.println(content+"\n");
	    	  pw.close();

		 
	       }catch(IOException ioe){
	    	   System.out.println("Exception occurred:");
	    	   ioe.printStackTrace();
	      }
	}
	
}
