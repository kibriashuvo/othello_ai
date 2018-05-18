import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Container;
import java.awt.EventQueue;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Map;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;

public class Othello extends JFrame {

	private JPanel contentPane;
	private Container contents;

	private JButton[][] squares = new JButton[8][8];

	private Color green = Color.GREEN;

	// ------------------------

	String initBoard = "###########........##........##........##...0X...##...X0...##........##........##........###########";
	InitGame ig;
	HashSet<String> move_list;
	// -----------------------

	private ImageIcon black = new ImageIcon("bullet-black.png");
	private ImageIcon white = new ImageIcon("bullet-grey.png");

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Othello frame = new Othello();
					frame.setVisible(true);
					frame.setDefaultCloseOperation(DISPOSE_ON_CLOSE);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});

	}

	/**
	 * Create the frame.
	 */
	public Othello() {
		
		super("Noob Othello");
		contents = getContentPane();
		contents.setLayout(new GridLayout(8, 8));
		ig = new InitGame();

		ActionListener btnhandler = new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub

				Object source = e.getSource();

				for (int i = 0; i < 8; i++) {
					for (int j = 0; j < 8; j++) {
						if (source == squares[i][j]) {

							ProcessClick(i, j);
						}

					}
				}

			}
		};

		for (int i = 0; i < 8; i++) {
			for (int j = 0; j < 8; j++) {
				squares[i][j] = new JButton();
				squares[i][j].setBackground(green);
				squares[i][j].addActionListener(btnhandler);
				contents.add(squares[i][j]);

			}
		}

		// ===================Init Game================
		initGame();

		// ============================================

		setSize(300, 300);
		setResizable(false);
		setLocationRelativeTo(null);
		setVisible(true);

	}

	// ========

	public void ProcessClick(int i, int j) {
		int row = i + 1;
		int col = j + 1;
	//	System.out.println(row + "" + col);

		if (checkMove(row + "" + col)) {
			makemove(row, col);
			try {
				TimeUnit.MILLISECONDS.sleep(2500);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			updateBoard();
			
			showMoves();

		}

	}

	public void executeScript(String board, String move) {
		String cmd = "c:\\Python34\\python.exe " + "othello.py " + board + " " + move;
		try {
			Process p = Runtime.getRuntime().exec(cmd);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public void showMoves() {
		BufferedReader br = null;
		move_list = new HashSet<String>();

		try {

			String sCurrentLine;

			br = new BufferedReader(new FileReader("valid_moves.txt"));

			while ((sCurrentLine = br.readLine()) != null) {
				if (sCurrentLine.equals(""))
					continue;
				move_list.add(sCurrentLine);

			}

		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				if (br != null)
					br.close();

			} catch (IOException ex) {
				ex.printStackTrace();
			}
		}

		for (String m : move_list) {
			if (move_list.isEmpty())
				break;
			int value = Integer.parseInt(m);
			int col = value % 10;
			int row = value / 10;
			squares[row - 1][col - 1].setBackground(Color.blue);

		}

	}

	public boolean checkMove(String mv) {
		if (move_list.contains(mv))
			return true;
		else
			return false;
	}

	public void initGame() {

		squares[3][4].setIcon(black);
		squares[3][3].setIcon(white);

		squares[4][3].setIcon(black);
		squares[4][4].setIcon(white);
		showMoves();
	}

	// ============File Write==================

	public static void writeFile(String content, String outputPath) {

		try {
			File file = new File(outputPath);
			if (!file.exists()) {
				file.createNewFile();
			}
			FileWriter fw = new FileWriter(file, true);
			BufferedWriter bw = new BufferedWriter(fw);
			PrintWriter pw = new PrintWriter(bw);
			pw.println(content + "\n");
			pw.close();

		} catch (IOException ioe) {
			System.out.println("Exception occurred:");
			ioe.printStackTrace();
		}
	}

	public void makemove(int row, int col) {
		try {
			Scanner in = new Scanner(new FileReader("othello_board.txt"));
			String board = in.nextLine();
			executeScript(board, row + "" + col);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public void updateBoard() {
		HashMap<Integer, Integer> map = ig.textToBoard();
		Iterator it = map.entrySet().iterator();
		while (it.hasNext()) {
			Map.Entry<Integer, Integer> pair = (Map.Entry<Integer, Integer>) it.next();
			int place = pair.getKey();
			int col = (place % 10) - 1;
			int row = (place / 10) - 1;

			int guti = pair.getValue();
			squares[row][col].setBackground(green);

			// System.out.println(row+""+col+"= "+place+"Guti = "+guti);

			if (guti == 0)
				continue;
			else if (guti == 1)
				squares[row][col].setIcon(white);
			else if (guti == 2)
				squares[row][col].setIcon(black);
			it.remove();

		}
	}

	public void printBoard(String board,String move) {
		int line_break = 0;
		int played_move = Integer.parseInt(move);
		for (int i = 0; i < 100; i++) {
			if(i==played_move){
				System.out.print('X');
				continue;
			}
			System.out.print(board.charAt(i));
			line_break++;
			if (line_break == 0) {
				System.out.println();
				line_break = 0;
			}
		}
	}
	
	

}
