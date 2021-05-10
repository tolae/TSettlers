package echo_client.messages;

import echo_client.EchoMessage;

import java.util.*;

public class EchoMessageFIFO implements Queue<EchoMessage> {
    private EchoMessage[] fifo;
    private int back;

    public EchoMessageFIFO(int size) {
        fifo = new EchoMessage[size];
        back = 0;
    }

    @Override
    public int size() {
        return back;
    }

    @Override
    public boolean isEmpty() {
        return back == fifo.length;
    }

    @Override
    public boolean contains(Object o) {
        return Arrays.asList(fifo).contains(o);
    }

    @Override
    public Iterator<EchoMessage> iterator() {
        return Arrays.asList(fifo).iterator();
    }

    @Override
    public Object[] toArray() {
        return fifo;
    }

    @Override
    public <T> T[] toArray(T[] a) {
        return Arrays.asList(fifo).toArray(a);
    }

    @Override
    public boolean add(EchoMessage echoMessage) {
        if (back < fifo.length) {
            fifo[back] = echoMessage;
            back += 1;
            return true;
        }
        return false;
    }

    @Override
    public boolean remove(Object o) {
        back -= 1;
        return Arrays.asList(fifo).remove(o);
    }

    @Override
    public boolean containsAll(Collection<?> c) {
        return Arrays.asList(fifo).containsAll(c);
    }

    @Override
    public boolean addAll(Collection<? extends EchoMessage> c) {
        if (back + c.size() < fifo.length) {
            back += c.size();
            Arrays.asList(fifo).addAll(c);
            return true;
        }
        return false;
    }

    @Override
    public boolean removeAll(Collection<?> c) {
        if (back - c.size() > 0) {
            back -= c.size();
            return Arrays.asList(fifo).removeAll(c);
        }
        return false;
    }

    @Override
    public boolean retainAll(Collection<?> c) {
        if (c.size() - 1 < fifo.length) {
            back = c.size() - 1;
            return Arrays.asList(fifo).retainAll(c);
        }
        return false;
    }

    @Override
    public void clear() {
        back = 0;
    }

    @Override
    public boolean offer(EchoMessage echoMessage) {
        return add(echoMessage);
    }

    @Override
    public EchoMessage remove() throws NoSuchElementException {
        if (back == 0) {
            throw new NoSuchElementException();
        }

        EchoMessage toRet = fifo[0];
        back -= 1;
        if (back >= 0) System.arraycopy(fifo, 1, fifo, 0, back);
        return toRet;
    }

    @Override
    public EchoMessage poll() {
        if (back == 0) {
            return null;
        }

        return remove();
    }

    @Override
    public EchoMessage element() throws NoSuchElementException {
        if (back == 0) {
            throw new NoSuchElementException();
        }

        return fifo[0];
    }

    @Override
    public EchoMessage peek() {
        if (back == 0) {
            return null;
        }

        return fifo[0];
    }
}
