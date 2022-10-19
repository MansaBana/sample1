#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h> // (or others, depending on the system in use)
#include <bits/stdc++.h>
#define f first
#define s second
using namespace std;

int a,b,c,d;
void init (void)
{
	glClearColor (1.0, 1.0, 1.0, 0.0); // Set display-window color to white.
	glMatrixMode (GL_PROJECTION); // Set projection parameters.
	gluOrtho2D (0, 500, 500, 1);// Orthogonal projection: [x,y,z]--->[x,y,0]
}

void line_draw(){
    vector<pair<int,int>> vec,vet;
    vec.push_back({a,b});
    vec.push_back({c,d});
    sort(vec.begin(),vec.end());
    vet.push_back({b,a});
    vet.push_back({d,c});
    int dx=vec[1].f-vec[0].f;
    int dy=vec[1].s-vec[0].s;
    sort(vet.begin(),vet.end());
    if(abs(dx)>abs(dy)){
        if(dy>0){
            int d=2*dy-dx,de=2*dy,dne=2*(dy-dx),x=vec[0].f,y=vec[0].s;
            glVertex2i(x,y);
            while(x<vec[1].f){
                if(d<=0){
                    d=d+de;
                    x=x+1;
                }
                else{
                    d=d+dne;
                    x=x+1;
                    y=y+1;
                }
                glVertex2i(x,y);
            }
        }
        else{
            int d=2*dy+dx,de=2*dy,dse=2*(dy+dx),x=vec[0].f,y=vec[0].s;
            glVertex2i(x,y);
            while(x<vec[1].f){
                if(d<=0){
                    d=d+dse;
                    x=x+1;
                    y=y-1;
                }
                else{
                    d=d+de;
                    x=x+1;
                }
                glVertex2i(x,y);
            }
        }
    }
    else{
        dx=vet[1].f-vet[0].f;
        dy=vet[1].s-vet[0].s;
        if(dy>0){
            int d=2*dy-dx,de=2*dy,dne=2*(dy-dx),x=vet[0].f,y=vet[0].s;
            glVertex2i(y,x);
            while(x<vet[1].f){
                if(d<=0){
                    d=d+de;
                    x=x+1;
                }
                else{
                    d=d+dne;
                    x=x+1;
                    y=y+1;
                }
                glVertex2i(y,x);
            }
        }
        else{
            int d=2*dy+dx,de=2*dy,dse=2*(dy+dx),x=vet[0].f,y=vet[0].s;
            glVertex2i(y,x);
            while(x<vet[1].f){
                if(d<=0){
                    d=d+dse;
                    x=x+1;
                    y=y-1;
                }
                else{
                    d=d+de;
                    x=x+1;
                }
                glVertex2i(y,x);
            }
        }
    }
}

void dispPoint (void)
{
	glClear (GL_COLOR_BUFFER_BIT); // Clear display window.
	glColor3f (1.0, 0.0, 0.0); // Set point color to green.
	glPointSize(1.0f); // Set point size
	glBegin(GL_POINTS);// Marks the beginning of the vertices list
    line_draw();
	glEnd( );
	glFlush( );
}
int main (int argc, char** argv)
{
	cin>>a>>b>>c>>d;
	glutInit (&argc, argv); // Initialize GLUT.
	glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB); // Set display mode.
	glutInitWindowPosition (10, 30); // Set top-left display-window position.
	glutInitWindowSize (500, 500); // Set display-window width and height.
	glutCreateWindow("Midpoint Line Drawing Algorithm"); // Create display window.
	init ( ); // Execute initialization procedure.
	glutDisplayFunc(dispPoint); // Send graphics to display window.
	glutMainLoop ( ); // Display everything and wait.
}
